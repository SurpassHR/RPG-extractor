import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from tools.loggers.simple_logger import loggerPrint

def getAllFilesFromFolder(folderPath: str) -> list[str]:
    if os.path.exists(folderPath):
        return []
    return os.listdir(folderPath)

def getFilesInFolderByType(folderPath: str, fileExt: str) -> list[str]:
    fileList = getAllFilesFromFolder(folderPath)
    fileList = [file for file in fileList if os.path.splitext(file)[1] == fileExt]
    fileList = [os.path.join(folderPath, file) for file in fileList]
    return fileList

def getFileInFolderByTypes(folderPath: str, fileExts: list[str]) -> list[str]:
    ret: list[str] = []
    for ext in fileExts:
        fileList = getFilesInFolderByType(folderPath, ext)
        if fileList:
            ret.extend(fileList)

    return ret