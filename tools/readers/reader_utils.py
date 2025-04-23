import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from tools.loggers.simple_logger import loggerPrint
from tools.public_def.level_defs import LogLevels

def isFolder(path: str) -> bool:
    return os.path.isdir(path)

def isFile(path: str) -> bool:
    isFile = os.path.isfile(path)
    if not isFile:
        loggerPrint(f'Path {path} is not a file.', level=LogLevels.WARNING)
    return isFile

def getFileName(path: str) -> str:
    return os.path.basename(path)

def getFileNameWithoutExt(path) -> str:
    return getFileName(path).split('.')[0]

def getFileExt(path: str) -> str:
    return os.path.splitext(path)[1]

def isPathExists(path: str) -> bool:
    return os.path.exists(path)

def isFolderExists(path: str) -> bool:
    if not isFolder(path):
        loggerPrint(f'Path {path} is not a folder.', level=LogLevels.WARNING)
        return False
    return isPathExists(path)

def isFileExists(path: str) -> bool:
    if not isFile(path):
        loggerPrint(f'Path {path} is not a file.', level=LogLevels.WARNING)
        return False
    return isPathExists(path)

def getBufferedReader(path: str, bufferSize: int = 1024) -> object:
    if not isFileExists(path):
        return None
    return open(path, 'rb', buffering=bufferSize)

def isFileInListValid(fileList: list[str]) -> bool:
    if fileList is None or len(fileList) == 0:
        loggerPrint('File list is empty.', level=LogLevels.WARNING)
        return False

    for filePath in fileList:
        if not isFileExists(filePath):
            loggerPrint(f'File {filePath} does not exist.', level=LogLevels.WARNING)
            return False
    return True