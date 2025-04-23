# some reusable public function

import os
import threading
import zlib
import json
from rubymarshal.classes import RubyString

from .definitions import FileExt

PRINT_LIST_FLG = False
def printList(dataList: list, needPrint: bool) -> None:
    if not PRINT_LIST_FLG and not needPrint:
        return
    if dataList is not None and dataList != []:
        for item in dataList:
            print(item)

PRINT_DICT_FLG = True
def printDict(dataDict: dict, needPrint: bool) -> None:
    if not PRINT_DICT_FLG and not needPrint:
        return
    if dataDict is not None and dataDict != {}:
        for key, value in dataDict.items():
            print(f"{key}: {value}")

LIST_WRITE_FILE_FLG = True
file_lock = threading.Lock()
def writeListToFile(dataList: list, fileName: str, firstWrite: bool) -> None:
    if not LIST_WRITE_FILE_FLG:
        return

    with file_lock:
        if firstWrite:
            if os.path.exists(fileName):
                os.remove(fileName)
            if not os.path.exists(os.path.dirname(fileName)):
                os.mkdir(os.path.dirname(fileName))
        if dataList is not None and dataList != []:
            with open(fileName, 'a') as f:
                for item in dataList:
                    f.write(str(item) + '\n')

def writeDictToJsonFile(dataDict: dict, fileName: str) -> None:
    with file_lock:
        if os.path.exists(fileName):
            os.remove(fileName)
        if not os.path.exists(os.path.dirname(fileName)):
            os.mkdir(os.path.dirname(fileName))
    if dataDict is not None and dataDict != {}:
        with open(fileName, 'a') as f:
            json.dump(dataDict, f, ensure_ascii=False, indent=4)

def traverseListBytesDecode(dataList: list) -> list:
    def __decode(item) -> str:
        try:
            item = item.decode('utf-8')
        except:
            item = zlib.decompress(item).decode('utf-8')
        return item

    retList = []
    for item in dataList:
        if isinstance(item, list):
            retList.extend(traverseListBytesDecode(item))
            continue
        if isinstance(item, str):
            retList.append(item)
            continue
        if isinstance(item, RubyString):
            retList.append(item.text)
            continue
        if isinstance(item, bytes):
            item = __decode(item)
            retList.append(item)
            continue

    return retList

def getFileListFromPath(extractPath: str, fileType: FileExt) -> list:
    fileExt = fileType.value
    fileList = os.listdir(extractPath)
    fileList = [file for file in fileList if os.path.splitext(file)[1] == fileExt]
    fileList = [os.path.join(extractPath, file) for file in fileList]
    # fileList = [r'E:\code\my-code\RPG-data-extractor\example_data\Map011_doodads.rxdata']

    return fileList

def listDedup(dataList: list) -> list:
    tempDataList = []
    [tempDataList.append(item) for item in dataList if item not in tempDataList]
    return tempDataList

def hashableListDedup(dataList: list) -> list:
    return list(dict.fromkeys(dataList))

def nonSeqListDedup(dataList: list) -> list:
    return list(set(dataList))

def readJson(filePath: str) -> dict:
    with open(filePath, 'r', encoding='utf-8') as jsonFile:
        jsonContent = json.load(jsonFile)
    return jsonContent

def loadConfig() -> dict:
    configFilePath = os.path.join('.', 'config.json')
    if not os.path.exists(configFilePath):
        raise FileNotFoundError(f"Config file not found: {configFilePath}")

    return readJson(configFilePath)