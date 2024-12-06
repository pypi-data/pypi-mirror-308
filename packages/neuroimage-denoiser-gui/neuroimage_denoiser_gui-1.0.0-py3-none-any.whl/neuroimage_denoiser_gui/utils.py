from enum import Enum
import uuid
import pathlib

class FileStatus(Enum):
    QUEUED = "Queued"
    RUNNING = "Running"
    FINISHED = "Finished"
    EARLY_TERMINATED = "Early terminated"
    UNKOWN = "Unkown"
    NO_OUTPUT = "Unkown due to no output"
    ERROR = "Failed"
    ERROR_FILE_EXISTS = "Output file already exists"
    ERROR_NDENOISER_UNKOWN = "Unexpected Error in DENOISER"

    def Get_Color(fs):
        match (fs):
            case FileStatus.ERROR | FileStatus.ERROR_FILE_EXISTS | FileStatus.ERROR_NDENOISER_UNKOWN | FileStatus.EARLY_TERMINATED:
                return "red"
            case FileStatus.UNKOWN | FileStatus.NO_OUTPUT:
                return "light_orange"
            case FileStatus.RUNNING:
                return "grey"
            case FileStatus.FINISHED:
                return "green"
            case _:
                return ""

class QueuedFile:
    def __init__(self, path):
        self._path = pathlib.Path(path)
        if (not self._path.is_file()):
            raise ValueError("The given path is not a file")
        self.id = str(uuid.uuid4())
        self.status: FileStatus = FileStatus.QUEUED

    @property
    def basepath(self):
        return self._path.parent
    
    @property
    def filename(self):
        return self._path.name
    
    @property
    def path(self):
        return self._path
    

class FileQueue:
    def __init__(self):
        self._fileQueue = {}

    def __getitem__(self, key) -> QueuedFile:
        return self._fileQueue[key]
    
    def __setitem__(self, key, value):
        self._fileQueue[key] = value

    def AddFile(self, qf: QueuedFile):
        if qf.id not in self._fileQueue.keys():
            self._fileQueue[qf.id] = qf

    def remove(self, key):
        self._fileQueue.pop(key)

    def keys(self):
        return self._fileQueue.keys()

    def items(self):
        return self._fileQueue.items()
    
    def values(self):
        return self._fileQueue.values()

    def PopQueued(self) -> QueuedFile | None:
        for id, qf in self._fileQueue.items():
           if qf.status == FileStatus.QUEUED:
               return qf
        return None