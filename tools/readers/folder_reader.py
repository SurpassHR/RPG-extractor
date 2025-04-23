import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from tools.loggers.simple_logger import loggerPrint
from tools.public_def.level_defs import LogLevels
from tools.readers.reader_utils import (
    isFolderExists,
    isFile,
    getFileExt
)

def getAllFilesFromFolder(folderPath: str) -> list[str]:
    if not isFolderExists(folderPath):
        return []

    fileList = os.listdir(folderPath)
    loggerPrint(f'Folder {folderPath} contains {len(fileList)} files.', level=LogLevels.INFO)

    return fileList

def getFilesInFolderByType(folderPath: str, fileExt: str) -> list[str]:
    fileList = getAllFilesFromFolder(folderPath)
    fileList = [file for file in fileList if isFile(file) and getFileExt(file) == fileExt]
    fileList = [os.path.join(folderPath, file) for file in fileList]

    return fileList

def getFileInFolderByTypes(folderPath: str, fileExts: list[str]) -> list[str]:
    ret: list[str] = []
    for ext in fileExts:
        ret.extend(getFilesInFolderByType(folderPath, ext))

    return ret