PRINT_LIST_FLG = False
def printList(dataList: list, needPrint: bool):
    if not PRINT_LIST_FLG and not needPrint:
        return
    if dataList is not None and dataList != []:
        for item in dataList:
            print(item)

import os

LIST_WRITE_FILE_FLG = True
def writeListToFile(dataList: list, fileName: str):
    if not LIST_WRITE_FILE_FLG:
        return
    if os.path.exists(fileName):
        os.remove(fileName)
    if dataList is not None and dataList != []:
        with open(fileName, 'a') as f:
            for item in dataList:
                f.write(str(item) + '\n')

from rubymarshal.classes import RubyString

def traverseListBytesDecode(dataList: list):
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