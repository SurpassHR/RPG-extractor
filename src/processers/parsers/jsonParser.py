from enum import IntEnum
from src.loggers.simpleLogger import loggerPrint
from src.processers.parsers.parserBase import ParserBase
from src.utils.fileTools import writeListToFile
from src.utils.timeTools import getCurrTimeInFmt
from src.utils.decorators.execTimer import execTimer

class ContentAttrCode(IntEnum):
    TITLE = 101 # 标题
    OPTION = 102 # 选项
    TEXT_DISP = 401 # 文本显示

class JsonParser(ParserBase):
    def __init__(self):
        super().__init__()
        self.dataList: list = []

    def _procList(self, data: list):
        pass

    def _procDict(self, data: dict):
        pass

    def _traverseToFindTargetText(self, data: dict | list, targetCode: ContentAttrCode = ContentAttrCode.TEXT_DISP) -> list:
        res = []

        if isinstance(data, list):
            for item in data:
                if isinstance(item, list):
                    res.extend(self._traverseToFindTargetText(item, targetCode))
                    continue
                if isinstance(item, dict):
                    code = item.get('code')
                    if code and code == 401:
                        res.append(item)
                        continue
                    res.extend(self._traverseToFindTargetText(item, targetCode))
        elif isinstance(data, dict):
            for key in data.keys():
                val = data[key]
                if isinstance(val, list):
                    res.extend(self._traverseToFindTargetText(val, targetCode))
                    continue
                if isinstance(val, dict):
                    code = val.get('code')
                    if code and code == 401:
                        res.append(val)
                        continue
                    res.extend(self._traverseToFindTargetText(val, targetCode))

        return res

    @execTimer
    def parse(self, data: dict):
        [self.dataList.append(data[item]) for item in data if 'Map' in item]
        loggerPrint(f"Filtered {len(self.dataList)} data from raw data.")
        resList = self._traverseToFindTargetText(self.dataList)
        writeListToFile(
            resList,
            f"output/parser/json/{getCurrTimeInFmt('%y-%m-%d_%H-%M')}/atomJsonCode401.txt"
        )