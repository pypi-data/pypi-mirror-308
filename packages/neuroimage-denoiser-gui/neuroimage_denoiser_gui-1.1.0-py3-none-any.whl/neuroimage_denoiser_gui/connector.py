from tkinter import messagebox
import os
import re
import subprocess
import threading
import sys
import pathlib
from typing import IO

from .logger import Logger
from .utils import *

class Connector:

    thread: threading.Thread | None = None
    currentSubprocess: subprocess.CompletedProcess = None
    _threadStopRequest = False

    def ImportNDenoiser() -> bool:
        envs = []
        for p in os.environ["PATH"].split(";"):
            r = re.findall(r"(?<=\\envs\\)\w*", p)
            for x in r:
                if x not in envs: envs.append(x)
        Logger.info(f"Detected environments: {', '.join(envs)}")
        try:
            import neuroimage_denoiser as nd
        except ModuleNotFoundError:
            messagebox.showerror("Neuroimage Denoiser GUI", "Can't find the Neuroimage Denoiser module. Terminating")
            exit()
        Logger.info(f"Neuroimage Denoiser installed: True")
        return True
    
    def TestInstallation():
        def _run():
            Logger.info("Testing installation. This may take some seconds...")
            result = subprocess.run(["python", "-m", "neuroimage_denoiser"], env=os.environ.copy(), capture_output=True)
            re1 = re.search(r"(Neuroimage Denoiser)", result.stdout.decode("utf-8"))
            re2 = re.search(r"(positional arguments)", result.stdout.decode("utf-8"))
            if len(result.stderr) > 0:
                Logger.error(f"Neuroimage Denoiser was not found. The error was '{result.stderr.decode('utf-8')}'")
                return
            elif re1 and re2:
                Logger.info("Neuroimage Denoiser was found and seems to be working. Testing if CUDA is ready...")
            else:
                Logger.error("Neuroimage Denoiser was found, but it prompted an unexpected message")
                Logger.info(f"The message was '{result.stdout.decode('utf-8')}'")
                return
            
            try:
                import torch
            except ModuleNotFoundError:
                Logger.error("Torch was not found")
                return
            if not torch.cuda.is_available():
                Logger.error("CUDA is not available. It is NOT recommened to proceed")
                return
            Logger.info("CUDA is ready for use")


        t = threading.Thread(target=_run, daemon=True)
        t.start()


    def Denoise(fileQueue:FileQueue, outputPath: pathlib.Path, modelPath: pathlib.Path, invalidateQueueCallback):
        if outputPath is None or not outputPath.exists() or len(str(outputPath)) <= 3:
            Logger.error("Your output path is invalid")
            return
        if modelPath is None or not modelPath.exists():
            Logger.error("Your model path is invalid")
            return
        def _run():
            if (fileQueue.PopQueued() is None):
                Logger.info("There are no files in the queue")
                return
            Logger.info("---Starting Denoising---")
            while (fileQueue.PopQueued() is not None):
                if Connector._threadStopRequest:
                    Logger.error("You aborted denoising")
                    break
                qf = fileQueue.PopQueued()
                qf.status = FileStatus.RUNNING
                Logger.info(f"Denoising {qf.filename}")
                invalidateQueueCallback()
                if isinstance(qf, QueuedFile):
                    params = ["python", "-m", "neuroimage_denoiser", "denoise", "--path", str(qf.path), "--outputpath", str(outputPath), "--modelpath", str(modelPath)]
                elif isinstance(qf, QueuedFolder):
                    params = ["python", "-m", "neuroimage_denoiser", "denoise", "--path", str(qf.path), "--outputpath", str(outputPath), "--modelpath", str(modelPath), "--directory_mode"]
                else:
                    raise RuntimeError("A provided Queued Object has an invalid type")
                Logger.debug(" ".join(params))

                env = os.environ.copy()
                env["PYTHONIOENCODING"] = "utf-8" # Alive progress in Stephans code needs utf-8. By default, python uses the wrong encoding. Setting the encoding in subprocess Popen only enables a conversion afterwards
                Connector.currentSubprocess = subprocess.Popen(params, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", bufsize=-1)
                Connector.currentSubprocess.wait()
                Connector.ND_ProcessOutput(Connector.currentSubprocess.returncode, Connector.currentSubprocess.stdout, Connector.currentSubprocess.stderr, qf)
                Logger.info(f"Finished {qf.filename}")
                invalidateQueueCallback()
            Logger.info("---Finished Denoising---")
        Connector._threadStopRequest = False
        if Connector.Is_Denoising(): return
        Connector.thread = threading.Thread(target=_run, daemon=True)
        Connector.thread.start()

    def Is_Denoising():
        if Connector.thread is not None and Connector.thread.is_alive():
            return True
        return False
    
    def ND_ProcessOutput(returncode, stdout: IO[str], stderr: IO[str], qf: QueuedObject):
        if stdout is None or stdout == "None":
            qf.status = FileStatus.ERROR
            return
        if stderr is None or stderr == "None":
            qf.status = FileStatus.ERROR
            return
        status = []
        while (line := stderr.readline().removesuffix("\n")) != "":
            if("FutureWarning: You are using `torch.load` with `weights_only=False`" in line):
                Logger.info("Neuroimage Denoise issued FutureWarning on torch")
                Logger.debug(line)
                continue
            elif("torch.load(weights" in line):
                Logger.debug(line)
                continue
            elif(line.strip() == ""):
                continue
            else:
                Logger.error(f"An unkown error was triggered: {line}")
        while (line := stdout.readline().removesuffix("\n")) != "":
            Logger.debug(line)
            re1 = re.search(r"on ([0-9]{1,3}): Skipped (.+), because file already exists", line)
            re2 = re.search(r"on ([0-9]{1,3}): Skipped (.+), due to an unexpected error", line)
            re3 = re.search(r"on ([0-9]{1,3}): Saved image \(([^\)]+)\) as:", line)
            if(line.strip() == ""):
                continue
            elif re1:
                status.append(FileStatus.ERROR_FILE_EXISTS)
                Logger.error(f"Skipped {re1.groups(1)}, as the output file already exists")
            elif re2:
                status.append(FileStatus.ERROR_NDENOISER_UNKOWN)
                Logger.error(f"Unkown error on {re1.groups(1)}")
            elif re3:
                status.append(FileStatus.FINISHED)
            elif(re.search(r"\| [0-9]{0,3}\/[0-9]{0,3} \[[0-9]{1,3}\%\] in ", line)):
                status.append(FileStatus.FINISHED)
            else:
                Logger.info(f"Unparsed output from Image Denoiser: '{line}'")
        qf.status = FileStatus.Get_MostSignificant(status)
        if (qf.status == None):
            if returncode == 1:
                qf.status = FileStatus.EARLY_TERMINATED
            else:
                qf.status = FileStatus.NO_OUTPUT
    
    def TryCanceling():
        Connector._threadStopRequest = True
        _sp_running = False
        if Connector.currentSubprocess is not None and Connector.currentSubprocess.poll() is None:
            _sp_running = True
            Connector.currentSubprocess.terminate()
        if not _sp_running and (Connector.thread is None or not Connector.thread.is_alive()): 
            Logger.info("There is no denoising running")
        else:
            Logger.error("Canceled denoising")