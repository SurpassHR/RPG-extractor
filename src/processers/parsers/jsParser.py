import json
import re

from src.processers.parsers.parserBase import ParserBase
from src.utils.fileTools import dumpListToFile
from src.utils.timeTools import getCurrTimeInFmt
from src.utils.decorators.execTimer import timer
from src.utils.dataStructTools import getAtomObjFromObj

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
        dumpListToFile(
            resList,
            f"output/parser/js/{getCurrTimeInFmt('%y-%m-%d_%H-%M')}/pluginList.json"
        )

        resList = getAtomObjFromObj(resList)
        dumpListToFile(
            resList,
            f"output/parser/js/{getCurrTimeInFmt('%y-%m-%d_%H-%M')}/pluginList_parseAtomObj.json"
        )

        newList = []
        for item in resList:
            if isinstance(item, str) and (item[0] == '{' or item[0] == '['):
                newList.append(self._deepParse(item))
            else:
                newList.append(item)
        dumpListToFile(
            newList,
            f"output/parser/js/{getCurrTimeInFmt('%y-%m-%d_%H-%M')}/pluginList_parseClusterData.json"
        )

        resList = getAtomObjFromObj(newList)
        dumpListToFile(
            resList,
            f"output/parser/js/{getCurrTimeInFmt('%y-%m-%d_%H-%M')}/pluginList_parseAtomClusterData.json"
        )

        return resList