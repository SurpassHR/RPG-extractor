import json
import zlib
from typing import Any
from rubymarshal.classes import RubyObject, RubyString, UserDef

from src.loggers.simpleLogger import loggerPrint


def listDedup(dataList: list) -> list:
    tempDataList = []
    [tempDataList.append(item) for item in dataList if item not in tempDataList]
    return tempDataList


def hashableListDedup(dataList: list) -> list:
    return list(dict.fromkeys(dataList))


def nonSeqListDedup(dataList: list) -> list:
    return list(set(dataList))


def traverseListBytesDecode(dataList: list) -> list:
    def __decode(item) -> str:
        try:
            item = item.decode("utf-8")
        except Exception as _:
            item = zlib.decompress(item).decode("utf-8")
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


def _traverseListDict(obj: Any) -> list:
    if obj == "":
        return []

    if isinstance(obj, int):
        return [obj]

    retList = []

    def __extendRetList(extendData: list):
        if extendData is not None and extendData != []:
            retList.extend(extendData)

    def __procList(obj: list):
        for item in obj:
            res = _traverseListDict(item)
            __extendRetList(res)
        return retList

    def __procDict(obj: dict):
        keys = obj.keys()
        for key in keys:
            res = _traverseListDict(obj[key])
            __extendRetList(res)
        return retList

    if isinstance(obj, list):
        return __procList(obj)

    if isinstance(obj, dict):
        return __procDict(obj)

    if isinstance(obj, str):
        try:
            if obj[0] == "[" or obj[0] == "{":
                dataLoads = json.loads(obj)
                loggerPrint(dataLoads)
                if isinstance(dataLoads, list):
                    loggerPrint(dataLoads)
                    return __procList(dataLoads)
                if isinstance(dataLoads, dict):
                    loggerPrint(dataLoads)
                    return __procDict(dataLoads)
            else:
                return [obj]
        except Exception as _:
            return [obj]

    return retList


def getAtomObjFromObj(fileData) -> list:
    atomObjList: list = []
    if isinstance(fileData, str):
        atomObjList.extend(_traverseListDict(fileData))
        return atomObjList
    for item in fileData:
        try:
            res = _traverseListDict(item)
            atomObjList.extend(res)
        except Exception as e:
            loggerPrint(f"Error processing obj: {e}")
            continue

    return atomObjList


def _hasDeeperRubyObj(obj: RubyObject):
    rubyObjAttrs = obj.attributes
    return "RubyObject" in str(rubyObjAttrs)


def hasDeeperJsonObj(obj: dict | list):
    if isinstance(obj, dict):
        return any(isinstance(v, (dict, list)) for v in obj.values())
    elif isinstance(obj, list):
        return any(isinstance(item, (dict, list)) for item in obj)
    return False


def _traverseRubyObj(obj: RubyObject | Any) -> list[RubyObject]:
    if isinstance(obj, UserDef):
        return []

    retList = []

    def __extendRetList(extendData: list):
        if extendData is not None and extendData != []:
            retList.extend(extendData)

    def __procList(obj: list):
        # list需要保证每个进入递归的对象都是RubyObject
        for item in obj:
            res = _traverseRubyObj(item)
            __extendRetList(res)
        # loggerPrintList(retList)
        return retList

    def __procDict(obj: dict):
        keys = obj.keys()
        for key in keys:
            res = _traverseRubyObj(obj[key])
            __extendRetList(res)
        # loggerPrintList(retList)
        return retList

    def __procRubyObj(obj: RubyObject):
        if _hasDeeperRubyObj(obj):
            attrs = obj.attributes
            res = _traverseRubyObj(attrs)
            __extendRetList(res)
            # loggerPrintList(retList)
            return retList
        return [obj]

    # 可能是 list、dict或RubyObject
    if isinstance(obj, list):
        return __procList(obj)

    if isinstance(obj, dict):
        return __procDict(obj)

    if isinstance(obj, RubyObject):
        return __procRubyObj(obj)

    return retList


def getAtomObjFromRubyObj(fileData) -> list[RubyObject]:
    atomObjList: list[RubyObject] = []
    if isinstance(fileData, RubyObject):
        atomObjList.extend(_traverseRubyObj(fileData))
        return atomObjList
    for rubyObj in fileData:
        try:
            atomObjList.extend(_traverseRubyObj(rubyObj))
        except Exception as e:
            loggerPrint(f"Error processing RubyObject: {e}")
            continue

    return atomObjList
