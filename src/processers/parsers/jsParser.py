import json
import re

from typing import Any

from src.loggers.simpleLogger import loggerPrint
from src.processers.parsers.parserBase import ParserBase
from src.utils.fileTools import writeListToFile
from src.utils.timeTools import getCurrTimeInFmt
from src.utils.decorators.execTimer import timer

class JsParser(ParserBase):
    def __init__(self):
        super().__init__()

    def _getTargetFileKeyContent(self, data: str) -> str:
        if not data:
            return ''

        pattern = re.compile(r"var \$plugins =\n*(\[.*\])", flags=re.DOTALL) # re.S 包含回车换行
        res = re.findall(pattern, data)
        if not res or len(res) == 0:
            return ''

        return res[0]

    def _traverseListDict(self, obj: Any) -> list:
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
                res = self._traverseListDict(item)
                __extendRetList(res)
            return retList

        def __procDict(obj: dict):
            keys = obj.keys()
            for key in keys:
                res = self._traverseListDict(obj[key])
                __extendRetList(res)
            return retList

        if isinstance(obj, list):
            return __procList(obj)

        if isinstance(obj, dict):
            return __procDict(obj)

        if isinstance(obj, str):
            try:
                if obj[0] == '[' or obj[0] == '{':
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
            except:
                return [obj]

        return retList

    def _getAtomObjFromObj(self, fileData) -> list:
        atomObjList: list = []
        if isinstance(fileData, str):
            atomObjList.extend(self._traverseListDict(fileData))
            return atomObjList
        for item in fileData:
            try:
                res = self._traverseListDict(item)
                atomObjList.extend(res)
            except Exception as e:
                loggerPrint(f'Error processing obj: {e}')
                continue

        return atomObjList

    def _deepParse(self, data):
        # 处理字典类型
        if isinstance(data, dict):
            return {k: self._deepParse(v) for k, v in data.items()}

        # 处理列表类型
        if isinstance(data, list):
            return [self._deepParse(item) for item in data]

        # 处理字符串类型
        if isinstance(data, str):
            # 尝试解析字符串为JSON
            try:
                # 先移除字符串首尾空白（根据实际需求决定是否保留）
                stripped = data.strip()
                parsed = json.loads(stripped)
                # 递归处理解析后的结果
                return self._deepParse(parsed)
            except json.JSONDecodeError:
                # 解析失败时保留原始字符串
                # 可以在此处添加额外的转义处理逻辑
                return data

        # 其他类型直接返回
        return data

    @timer
    def parse(self, data: str) -> list:
        res = self._getTargetFileKeyContent(data)

        resList = json.loads(res)
        writeListToFile(
            resList,
            f"output/parser/js/{getCurrTimeInFmt('%y-%m-%d_%H-%M')}/pluginList.json"
        )

        resList = self._getAtomObjFromObj(resList)
        writeListToFile(
            resList,
            f"output/parser/js/{getCurrTimeInFmt('%y-%m-%d_%H-%M')}/pluginList_parseAtomObj.json"
        )

        newList = []
        for item in resList:
            if isinstance(item, str) and (item[0] == '{' or item[0] == '['):
                newList.append(self._deepParse(item))
            else:
                newList.append(item)
        writeListToFile(
            newList,
            f"output/parser/js/{getCurrTimeInFmt('%y-%m-%d_%H-%M')}/pluginList_parseClusterData.json"
        )

        resList = self._getAtomObjFromObj(newList)
        writeListToFile(
            resList,
            f"output/parser/js/{getCurrTimeInFmt('%y-%m-%d_%H-%M')}/pluginList_parseAtomClusterData.json"
        )

        return resList