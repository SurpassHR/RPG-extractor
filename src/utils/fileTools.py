import os
import json
from src.loggers.simpleLogger import loggerPrint
from src.publicDef.levelDefs import LogLevels

def readJson(filePath: str) -> dict:
    with open(filePath, 'r', encoding='utf-8') as jsonFile:
        jsonContent = json.load(jsonFile)
    return jsonContent

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
    return os.path.splitext(path)[1].replace('.', '')

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

def getAllFilesFromFolder(folderPath: str) -> list[str]:
    if not isFolderExists(folderPath):
        return []

    fileList = os.listdir(folderPath)
    fileList = [os.path.join(folderPath, file) for file in fileList]
    loggerPrint(f'Folder `{folderPath}` contains {len(fileList)} files.', level=LogLevels.INFO)

    return fileList

def getFilesInFolderByType(folderPath: str, fileExt: str) -> list[str]:
    fileList = getAllFilesFromFolder(folderPath)
    fileList = [file for file in fileList if isFile(file) and getFileExt(file) == fileExt]
    fileList = [os.path.join(folderPath, file) for file in fileList]

    return fileList

def getFilesInFolderByTypes(folderPath: str, fileExts: list[str]) -> list[str]:
    ret: list[str] = []
    for ext in fileExts:
        ret.extend(getFilesInFolderByType(folderPath, ext))

    return ret