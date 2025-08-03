from enum import IntEnum
from typing import Any

from src.loggers.simpleLogger import loggerPrint
from src.processers.parsers.parserBase import ParserBase
from src.utils.fileTools import dumpListToFile
from src.utils.timeTools import getCurrTimeInFmt
from src.utils.decorators.execTimer import timer
from src.utils.dataStructTools import hasDeeperJsonObj


class ContentAttrCode(IntEnum):
    TITLE = 101  # 标题
    OPTION = 102  # 选项
    TEXT_DISP = 401  # 文本显示


class ParseNeededFile:
    def __init__(self) -> None:
        self._mapFiles: dict[str, str] = {}
        self._itemFiles: dict[str, str] = {}
        self._specialFiles: dict[str, str] = {}

    def addMapFile(self, k: str, v: str) -> None:
        self._mapFiles[k] = v

    def addItemFile(self, k: str, v: str) -> None:
        self._itemFiles[k] = v

    def addSpecialFiles(self, k: str, v: str) -> None:
        self._specialFiles[k] = v

    def getMapFiles(self) -> dict:
        return self._mapFiles

    def getItemFiles(self) -> dict:
        return self._itemFiles

    def getSpecialFiles(self) -> dict:
        return self._specialFiles

    def getFileNum(self) -> int:
        return len(self._mapFiles) + len(self._itemFiles) + len(self._specialFiles)


class JsonParser(ParserBase):
    def __init__(self):
        super().__init__()
        self.parseNeededFile = ParseNeededFile()

    def _procList(self, data: list):
        pass

    def _procDict(self, data: dict):
        pass

    def _traverseToFindTargetObj(self, data: dict | list, targetK: list[str] | str, targetV: Any) -> list:
        res = []

        if isinstance(data, list):
            for item in data:
                if isinstance(item, list):
                    res.extend(self._traverseToFindTargetObj(item, targetK, targetV))
                    continue
                if isinstance(item, dict):
                    v = item.get(targetK)
                    if v and (v == targetV or targetV == "*"):
                        res.append(item)
                    res.extend(self._traverseToFindTargetObj(item, targetK, targetV))
        elif isinstance(data, dict):
            for key in data.keys():
                val = data[key]
                if isinstance(val, list):
                    res.extend(self._traverseToFindTargetObj(val, targetK, targetV))
                    continue
                if isinstance(val, dict):
                    v = val.get(targetK)
                    if v and (v == targetV or targetV == "*"):
                        res.append(val)
                    res.extend(self._traverseToFindTargetObj(val, targetK, targetV))

        return res

    def _traverseToGetTargetObj(self, data: dict | list, targetK: str, targetV: str) -> list:
        res = []

        if isinstance(data, list):
            for item in data:
                if isinstance(item, list):
                    res.extend(self._traverseToFindTargetObj(item, targetK, targetV))
                    continue
                if isinstance(item, dict):
                    v = item.get(targetK)
                    if v and (v == targetV or targetV == "*"):
                        res.append(v)
                        continue
                    res.extend(self._traverseToFindTargetObj(item, targetK, targetV))
        elif isinstance(data, dict):
            for key in data.keys():
                val = data[key]
                if isinstance(val, list):
                    res.extend(self._traverseToFindTargetObj(val, targetK, targetV))
                    continue
                if isinstance(val, dict):
                    v = val.get(targetK)
                    if v and (v == targetV or targetV == "*"):
                        res.append(v)
                        continue
                    res.extend(self._traverseToFindTargetObj(val, targetK, targetV))

        return res

    def _traverseToFindTargetAtomObj(self, data: dict | list, targetK: list[str] | str, targetV: Any) -> list:
        res = []

        if isinstance(data, list):
            for item in data:
                if isinstance(item, list):
                    res.extend(self._traverseToFindTargetObj(item, targetK, targetV))
                    continue
                if isinstance(item, dict):
                    v = item.get(targetK)
                    if v and (v == targetV or targetV == "*"):
                        res.append(v)
                    res.extend(self._traverseToFindTargetObj(item, targetK, targetV))
        elif isinstance(data, dict):
            for key in data.keys():
                val = data[key]
                if isinstance(val, list):
                    res.extend(self._traverseToFindTargetObj(val, targetK, targetV))
                    continue
                if isinstance(val, dict):
                    v = val.get(targetK)
                    if v and (v == targetV or targetV == "*"):
                        res.append(v)
                    res.extend(self._traverseToFindTargetObj(val, targetK, targetV))

        return res

    def _traverseToGetTargetAtomObj(self, data: dict | list, targetK: str, targetV: str) -> list:
        res = []

        if isinstance(data, list):
            for item in data:
                if isinstance(item, list):
                    res.extend(self._traverseToFindTargetAtomObj(item, targetK, targetV))
                    continue
                if isinstance(item, dict):
                    v = item.get(targetK)
                    if v and (v == targetV or targetV == "*"):
                        res.append(v)
                        continue
                    res.extend(self._traverseToFindTargetAtomObj(item, targetK, targetV))
        elif isinstance(data, dict):
            for key in data.keys():
                val = data[key]
                if isinstance(val, list):
                    res.extend(self._traverseToFindTargetAtomObj(val, targetK, targetV))
                    continue
                if isinstance(val, dict):
                    v = val.get(targetK)
                    if v and (v == targetV or targetV == "*"):
                        res.append(v)
                        continue
                    res.extend(self._traverseToFindTargetAtomObj(val, targetK, targetV))

        return res

    @timer
    def parse(self, data: dict) -> list:
        for k, v in data.items():
            if "Map" in k or "CommonEvents" in k:
                self.parseNeededFile.addMapFile(k, v)
                continue
            if "Items" in k:
                self.parseNeededFile.addItemFile(k, v)
                continue
            if "System" in k:
                self.parseNeededFile.addSpecialFiles(k, v)
                continue

        loggerPrint(f"Filtered {self.parseNeededFile.getFileNum()} data from raw data.")

        dialogueJsonCodeList = self._traverseToFindTargetObj(
            data=self.parseNeededFile.getMapFiles(), targetK="code", targetV=ContentAttrCode.TEXT_DISP.value
        )
        dialogueJsonCodeList.extend(
            self._traverseToFindTargetObj(
                data=self.parseNeededFile.getMapFiles(), targetK="code", targetV=ContentAttrCode.OPTION.value
            )
        )
        dialogueJsonCodeList.extend(
            self._traverseToFindTargetObj(
                data=self.parseNeededFile.getMapFiles(), targetK="code", targetV=ContentAttrCode.TITLE.value
            )
        )
        dumpListToFile(
            dialogueJsonCodeList, f"output/parser/json/{getCurrTimeInFmt('%y-%m-%d_%H-%M')}/dialogueJsonCodeList.json"
        )
        mapNameJsonCodeList = self._traverseToGetTargetObj(
            data=self.parseNeededFile.getMapFiles(), targetK="displayName", targetV="*"
        )
        dumpListToFile(
            mapNameJsonCodeList,
            f"output/parser/json/{getCurrTimeInFmt('%y-%m-%d_%H-%M')}/mapDisplayNameJsonCodeList.json",
        )

        itemJsonCodeList = self._traverseToFindTargetObj(
            data=self.parseNeededFile.getItemFiles(), targetK="name", targetV="*"
        )
        dumpListToFile(
            itemJsonCodeList, f"output/parser/json/{getCurrTimeInFmt('%y-%m-%d_%H-%M')}/itemJsonCodeList.json"
        )

        specialJsonCodeList: list = []
        specialKeyList = [
            "name",
            "switches",
            "basic",
            "commands",
            "params",
            "variables",
        ]
        for k in specialKeyList:
            specialJsonCodeList.extend(
                self._traverseToGetTargetAtomObj(data=self.parseNeededFile.getSpecialFiles(), targetK=k, targetV="*")
            )
        dumpListToFile(
            specialJsonCodeList, f"output/parser/json/{getCurrTimeInFmt('%y-%m-%d_%H-%M')}/specialJsonCodeList.json"
        )

        rawDataList: list = []
        for item in dialogueJsonCodeList:
            code = item.get("code")
            if code == ContentAttrCode.TEXT_DISP.value:
                rawDataList.append(item["parameters"][0])
                continue
            if code == ContentAttrCode.OPTION.value:
                rawDataList.extend(item["parameters"][0])
                continue
            if code == ContentAttrCode.TITLE.value:
                rawDataList.append(item["parameters"][-1])
                continue

        for item in itemJsonCodeList:
            if item.get("name"):  # 确保 item['name'] 不是假值，避免意外情况
                rawDataList.append(item["name"])
            if item.get("description"):  # 确保 item['description'] 不是假值
                rawDataList.append(item["description"])

        for item in specialJsonCodeList:
            if isinstance(dict, str) and item.get("name"):
                rawDataList.append(item["name"])
            if isinstance(item, list) and not hasDeeperJsonObj(item):
                rawDataList.extend(item)

        rawDataList.extend(mapNameJsonCodeList)

        rawDataList = [item for item in rawDataList if item and item != ""]
        dumpListToFile(rawDataList, f"output/parser/json/{getCurrTimeInFmt('%y-%m-%d_%H-%M')}/rawDataList.json")

        return rawDataList
