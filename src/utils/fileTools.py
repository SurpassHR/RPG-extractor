import os
import json
import threading

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

def getFileParentFolder(path: str) -> str:
    return os.path.split(os.path.dirname(path))[-1]

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

list_file_lock = threading.Lock()
def dumpListToFile(dataList: list, fileName: str, firstWrite: bool = True) -> None:
    with list_file_lock:
        if firstWrite:
            if os.path.exists(fileName):
                os.remove(fileName)
            if not os.path.exists(os.path.dirname(fileName)):
                os.makedirs(os.path.dirname(fileName))
        if dataList is not None and dataList != []:
            with open(fileName, 'a', encoding='utf-8') as f:
                dataList = [item for item in dataList if item != '']
                json.dump(dataList, f, ensure_ascii=False, indent=4)

def writeListToFile(dataList: list, fileName: str, firstWrite: bool = True) -> None:
    with list_file_lock:
        if firstWrite:
            if os.path.exists(fileName):
                os.remove(fileName)
            if not os.path.exists(os.path.dirname(fileName)):
                os.makedirs(os.path.dirname(fileName))
        if dataList is not None and dataList != []:
            with open(fileName, 'a') as f:
                for item in dataList:
                    f.write(str(item) + '\n')

dict_file_lock = threading.Lock()
def writeDictToJsonFile(dataDict: dict, fileName: str, firstWrite: bool = True) -> None:
    with dict_file_lock:
        if firstWrite:
            if os.path.exists(fileName):
                os.remove(fileName)
            if not os.path.exists(os.path.dirname(fileName)):
                os.makedirs(os.path.dirname(fileName))
    if dataDict is not None and dataDict != {}:
        with open(fileName, 'a', encoding='utf-8') as f:
            json.dump(dataDict, f, ensure_ascii=False, indent=4)
            f.write('\n')

ruby_file_lock = threading.Lock()
def writeListToRubyFile(dataList: list, fileName: str, firstWrite: bool = True) -> None:
    with ruby_file_lock:
        if firstWrite:
            if os.path.exists(fileName):
                os.remove(fileName)
            if not os.path.exists(os.path.dirname(fileName)):
                os.makedirs(os.path.dirname(fileName))
    with open(fileName, 'a') as rbFile:
        for item in dataList:
            if not item:
                continue
            rbFile.write('{}'.format(item.replace('\r', '')))

class FileTool:
    def __init__(self) -> None:
        pass

    def _exportListToJson(self, data: list, exportJson: str) -> None:
        jsonContent: dict = {}
        for item in data:
            key = val = f'{item}'
            jsonContent[key] = val

        writeDictToJsonFile(jsonContent, exportJson, True)