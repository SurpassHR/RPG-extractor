import re

from src.processers.formatters.formatterBase import FormatterBase
from src.utils.fileTools import writeListToFile
from src.utils.timeTools import getCurrTimeInFmt
from src.utils.regexTools import execMultiReSub

class JsonFormatter(FormatterBase):
    def __init__(self):
        super().__init__()

    def _rmAllNameTile(self, dataList: list[str]) -> list[str]:
        patternDict: dict[re.Pattern[str], str] = {
            re.compile(r'\\n[cr]*<\\c\[\d{1,3}\].*\\c>'): '',
            re.compile(r'\\\w\[\d{1,3}\]'): '\n',
            re.compile(r'\\c'): '\n'
        }

        subbedDataList: list[str] = []
        for item in dataList:
            subbedDataList.append(execMultiReSub(patternDict, item))

        return subbedDataList

    def listDedup(self, dataList: list) -> list:
        tempDataList = []
        [tempDataList.append(item) for item in dataList if item not in tempDataList]
        return tempDataList

    def hashableListDedup(self, dataList: list) -> list:
        return list(dict.fromkeys(dataList))

    def nonSeqListDedup(self, dataList: list) -> list:
        return list(set(dataList))

    def format(self, data: list):
        res: list = self._rmAllNameTile(data)
        writeListToFile(
            res,
            f"output/formatter/json/{getCurrTimeInFmt('%y-%m-%d_%H-%M')}/textDisp_NoTitle.json"
        )

        res: list = self.hashableListDedup(res)
        writeListToFile(
            res,
            f"output/formatter/json/{getCurrTimeInFmt('%y-%m-%d_%H-%M')}/textDisp_NoTitle_Dedup.json"
        )

        res: list = self._restoreIncorrectLineBreaks(res)
        writeListToFile(
            res,
            f"output/formatter/json/{getCurrTimeInFmt('%y-%m-%d_%H-%M')}/textDisp_NoTitle_Dedup_FixLineBreak.json"
        )

        return res