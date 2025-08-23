from src.processers.formatters.formatterBase import FormatterBase, jsonPatternDict
from src.utils.fileTools import dumpListToFile
from src.utils.timeTools import getCurrTimeInFmt
from src.utils.regexTools import execMultiReSub
from src.utils.dataStructTools import hashableListDedup


class JsonFormatter(FormatterBase):
    def __init__(self):
        super().__init__()

    def _rmAllEscapes(self, dataList: list[str]) -> list[str]:
        subbedDataList: list[str] = []
        for item in dataList:
            data = execMultiReSub(jsonPatternDict, str(item))
            subbedDataList.append(data)

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
