import os
import threading
from rubymarshal.classes import RubyString
from definitions import FileType

PRINT_LIST_FLG = False
def printList(dataList: list, needPrint: bool) -> None:
    if not PRINT_LIST_FLG and not needPrint:
        return
    if dataList is not None and dataList != []:
        for item in dataList:
            print(item)

LIST_WRITE_FILE_FLG = True
file_lock = threading.Lock()
def writeListToFile(dataList: list, fileName: str, firstWrite: bool) -> None:
    if not LIST_WRITE_FILE_FLG:
        return

    with file_lock:
        if firstWrite and os.path.exists(fileName):
            os.remove(fileName)

        if dataList is not None and dataList != []:
            with open(fileName, 'a') as f:
                for item in dataList:
                    f.write(str(item) + '\n')

def traverseListBytesDecode(dataList: list) -> list:
    retList = []
    for item in dataList:
        if isinstance(item, list):
            retList.extend(traverseListBytesDecode(item))
            continue
        if isinstance(item, str | RubyString):
            retList.append(item)
            continue
        if isinstance(item, bytes):
            item = item.decode('utf-8')
            retList.append(item)
            continue

    return retList

def getFileListFromPath(extractPath: str, fileType: FileType) -> list:
    fileExt = fileType.value
    fileList = os.listdir(extractPath)
    fileList = [file for file in fileList if os.path.splitext(file)[1] == fileExt]
    fileList = [os.path.join(extractPath, file) for file in fileList]

    return fileList

def listDedup(dataList: list) -> list:
    tempDataList = []
    [tempDataList.append(item) for item in dataList if item not in tempDataList]

    return tempDataList