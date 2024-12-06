from tkinter import messagebox
import os
import re
import subprocess
import threading
import time
import pathlib
from io import StringIO
from typing import IO

from .logger import Logger
from .utils import QueuedFile,FileQueue, FileStatus

class Connector:

    thread: threading.Thread | None = None
    currentSubprocess: subprocess.Popen = None
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
        if outputPath is None or not outputPath.exists():
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
                params = ["python", "-m", "neuroimage_denoiser", "denoise", "--path", str(qf.path), "--outputpath", str(outputPath), "--modelpath", str(modelPath)]

                Connector.currentSubprocess = subprocess.Popen(params, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8")   
                Connector.currentSubprocess.wait()
                Connector.ND_ProcessOutput(Connector.currentSubprocess.returncode, Connector.currentSubprocess.stdout, Connector.currentSubprocess.stderr, qf)
                #Connector.ND_ProcessOutput(stdout, Connector.currentSubprocess.stderr, qf)
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
    
    def ND_ProcessOutput(returncode, stdout: IO[str], stderr: IO[str], qf: QueuedFile):
        if stdout is None or stdout == "None":
            qf.status = FileStatus.ERROR
            return
        if stderr is None or stderr == "None":
            qf.status = FileStatus.ERROR
            return
        
        while (line := stderr.readline().removesuffix("\n")) != "":
            if("FutureWarning: You are using `torch.load` with `weights_only=False`" in line):
                Logger.info("Neuroimage Denoise issued FutureWarning on torch")
                continue
            elif("torch.load(weights" in line):
                continue
            elif(line.strip() == ""):
                continue
            else:
                Logger.error(f"An unkown error was triggered: {line}")
        qf.status = FileStatus.EARLY_TERMINATED
        while (line := stdout.readline().removesuffix("\n")) != "":
            if(re.search(r"(Skipped )(\w+)(, because file already exists)", line)):
                qf.status = FileStatus.ERROR_FILE_EXISTS
                return
            elif(re.search(r"(Skipped )(\w+)(, due to an unexpected error)", line)):
                qf.status = FileStatus.ERROR_NDENOISER_UNKOWN
                return
            elif(line.strip() == ""):
                continue
            elif("Saved image " in line):
                qf.status = FileStatus.FINISHED
            elif(re.search(r"\| [0-9]{0,3}\/[0-9]{0,3} \[[0-9]{1,3}\%\] in ", line)):
                qf.status = FileStatus.FINISHED
            else:
                Logger.info(f"Unparsed output from Image Denoiser: '{line}'")
        if (qf.status == FileStatus.EARLY_TERMINATED and returncode != 1):
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
            Logger.info("Trying to abort denoising...")