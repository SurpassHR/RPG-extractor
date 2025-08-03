import re

from src.processers.formatters.formatterBase import FormatterBase
from src.utils.fileTools import dumpListToFile
from src.utils.timeTools import getCurrTimeInFmt
from src.utils.regexTools import execMultiReSub
from src.utils.dataStructTools import hashableListDedup


class JsonFormatter(FormatterBase):
    def __init__(self):
        super().__init__()

    def _rmAllEscapes(self, dataList: list[str]) -> list[str]:
        patternDict: dict[re.Pattern[str], str] = {
            re.compile(r"\\n[cr]*<\\c\[\d{1,3}\].*\\c>"): "",
            re.compile(r"\\\w\[\d{1,3}\]"): "\n",
            re.compile(r"\\CR"): "\n",
            re.compile(r"\\c"): "\n",
        }

        subbedDataList: list[str] = []
        for item in dataList:
            subbedDataList.append(execMultiReSub(patternDict, item))

        return subbedDataList

    def format(self, data: list):
        res: list = self._rmAllEscapes(data)
        dumpListToFile(res, f"output/formatter/json/{getCurrTimeInFmt('%y-%m-%d_%H-%M')}/textDisp_NoTitle.json")

        res: list = hashableListDedup(res)
        dumpListToFile(res, f"output/formatter/json/{getCurrTimeInFmt('%y-%m-%d_%H-%M')}/textDisp_NoTitle_Dedup.json")

        res: list = self._restoreIncorrectLineBreaks(res)
        dumpListToFile(
            res, f"output/formatter/json/{getCurrTimeInFmt('%y-%m-%d_%H-%M')}/textDisp_NoTitle_Dedup_FixLineBreak.json"
        )

        return res
