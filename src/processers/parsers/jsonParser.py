from enum import IntEnum
from typing import Any

from src.loggers.simpleLogger import loggerPrint
from src.processers.parsers.parserBase import ParserBase
from src.utils.fileTools import dumpListToFile
from src.utils.timeTools import getCurrTimeInFmt
from src.utils.decorators.execTimer import timer
from src.utils.dataStructTools import hasDeeperJsonObj
from src.publicDef.levelDefs import LogLevels


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
        """
        解析原始数据字典，提取所有需要翻译的文本。
        重构后的版本，提高了可读性、性能和可维护性。
        """
        # 1. 分类数据
        self._classify_data(data)
        loggerPrint(f"Filtered {self.parseNeededFile.getFileNum()} data from raw data.")

        # 2. 提取各类文本
        map_texts = self._extract_map_texts()
        item_texts = self._extract_item_texts()
        special_texts = self._extract_special_texts()

        # 3. 聚合和清洗数据
        raw_data_list = map_texts + item_texts + special_texts

        # 移除所有空值或仅包含空白的字符串
        cleaned_data = [item for item in raw_data_list if isinstance(item, str) and item and not item.isspace()]

        # 4. (可选) 导出调试文件
        self._dump_debug_files(
            {
                "dialogue_and_map_name": map_texts,
                "items": item_texts,
                "special": special_texts,
                "all_raw_text": cleaned_data,
            }
        )

        return cleaned_data

    def _classify_data(self, data: dict):
        """根据关键字将数据分类到 parseNeededFile 对象中。"""
        for k, v in data.items():
            if "Map" in k or "CommonEvents" in k:
                self.parseNeededFile.addMapFile(k, v)
            elif "Items" in k:
                self.parseNeededFile.addItemFile(k, v)
            elif "System" in k:
                self.parseNeededFile.addSpecialFiles(k, v)

    def _extract_map_texts(self) -> list:
        """从地图和公共事件数据中提取文本。"""
        map_files = self.parseNeededFile.getMapFiles()
        if not map_files:
            return []

        texts = []

        # 提取地图显示名称
        map_names = self._traverseToGetTargetObj(data=map_files, targetK="displayName", targetV="*")
        texts.extend(map_names)

        # 提取对话、选项和标题文本
        dialogue_codes = [ContentAttrCode.TEXT_DISP.value, ContentAttrCode.OPTION.value, ContentAttrCode.TITLE.value]

        event_commands = []
        for code_val in dialogue_codes:
            event_commands.extend(self._traverseToFindTargetObj(data=map_files, targetK="code", targetV=code_val))

        for item in event_commands:
            code = item.get("code")
            parameters = item.get("parameters")
            if not parameters:
                continue

            try:
                if code == ContentAttrCode.TEXT_DISP.value:
                    texts.append(parameters[0])
                elif code == ContentAttrCode.OPTION.value and isinstance(parameters[0], list):
                    texts.extend(parameters[0])
                elif code == ContentAttrCode.TITLE.value:
                    texts.append(parameters[-1])
            except (IndexError, TypeError) as e:
                loggerPrint(f"Error processing event command {item}: {e}", level=LogLevels.WARNING)

        return texts

    def _extract_item_texts(self) -> list:
        """从物品数据中提取名称和描述。"""
        item_files = self.parseNeededFile.getItemFiles()
        if not item_files:
            return []

        texts = []
        item_list = self._traverseToFindTargetObj(data=item_files, targetK="name", targetV="*")

        for item in item_list:
            if isinstance(item, dict):
                if name := item.get("name"):
                    texts.append(name)
                if description := item.get("description"):
                    texts.append(description)
        return texts

    def _extract_special_texts(self) -> list:
        """从系统数据中提取各种文本。"""
        special_files = self.parseNeededFile.getSpecialFiles()
        if not special_files:
            return []

        texts = []
        specialKeyList = ["name", "switches", "basic", "commands", "params", "variables"]

        found_items = []
        for k in specialKeyList:
            found_items.extend(self._traverseToGetTargetAtomObj(data=special_files, targetK=k, targetV="*"))

        for item in found_items:
            if isinstance(item, dict):
                if name := item.get("name"):
                    texts.append(name)
            # 提取扁平化的字符串列表
            elif isinstance(item, list) and not hasDeeperJsonObj(item):
                texts.extend(filter(lambda x: isinstance(x, str), item))

        return texts

    def _dump_debug_files(self, data_map: dict):
        """将提取过程中的中间数据和最终结果导出为JSON文件以供调试。"""
        timestamp = getCurrTimeInFmt("%y-%m-%d_%H-%M")
        outputDir = f"output/parser/json/{timestamp}"

        for name, data in data_map.items():
            dumpListToFile(data, f"{outputDir}/{name}.json")

        self._setStageDataPath(f"{outputDir}/all_raw_text.json")
