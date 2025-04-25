import os
import json

def readJson(filePath: str) -> dict:
    with open(filePath, 'r', encoding='utf-8') as jsonFile:
        jsonContent = json.load(jsonFile)
    return jsonContent

def isFolder(path: str) -> bool:
    return os.path.isdir(path)

def isFile(path: str) -> bool:
    return os.path.isfile(path)

def getFileName(path: str) -> str:
    return os.path.basename(path)

def getFileNameWithoutExt(path) -> str:
    return getFileName(path).split('.')[0]

def getFileExt(path: str) -> str:
    return os.path.splitext(path)[1].replace('.', '')

def isPathExists(path: str) -> bool:
    return os.path.exists(path)

def isFolderExists(path: str) -> bool:
    return os.path.isdir(path) and os.path.exists(path)

def isFileExists(path: str) -> bool:
    return os.path.isfile(path) and os.path.exists(path)

def getBufferedReader(path: str, bufferSize: int = 1024) -> object:
    if not isFileExists(path):
        return None
    return open(path, 'rb', buffering=bufferSize)

def isFileInListValid(fileList: list[str]) -> bool:
    if fileList is None or len(fileList) == 0:
        return False

    for filePath in fileList:
        if not isFileExists(filePath):
            return False
    return True

def getAllFilesFromFolder(folderPath: str) -> list[str]:
    if not isFolderExists(folderPath):
        return []

    fileList = os.listdir(folderPath)
    fileList = [os.path.join(folderPath, file) for file in fileList]

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