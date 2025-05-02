import re
from rubymarshal.classes import RubyString

from src.loggers.simpleLogger import loggerPrint
from src.publicDef.levelDefs import LogLevels
from src.processers.formatters.formatterBase import FormatterBase
from src.utils.dataStructTools import hashableListDedup, listDedup
from src.utils.timeTools import getCurrTimeInFmt
from src.utils.decorators.execTimer import timer
from src.utils.regexTools import execMultiReSub

class RxdataFormatter(FormatterBase):
    def __init__(self):
        super().__init__()

    def _sentenceJoint(self, strList: list[str]):
        return self._restoreIncorrectLineBreaks(strList)

    def _rmAllEscapes(self, dataList: list[str]) -> list[str]:
        patternDict: dict[re.Pattern[str], str] = {
            re.compile(r'\\[a-zA-Z]\[\d+\]'): '\n',
            re.compile(r'\n{2,}'): '\n',
        }

        subbedDataList: list[str] = []
        for item in dataList:
            try:
                if isinstance(item, list):
                    subbedDataList.append(execMultiReSub(patternDict, str(item)))
                    continue
                if isinstance(item, RubyString):
                    subbedDataList.append(execMultiReSub(patternDict, item.text))
                    continue
                else:
                    subbedDataList.append(execMultiReSub(patternDict, item))
            except:
                loggerPrint(f"{item}, {type(item)}", level=LogLevels.WARNING)

        return subbedDataList

    @timer
    def format(self, data: tuple[list, list]) -> list:
        dialogueList, optionList = data
        jointedSentences = self._sentenceJoint(dialogueList)

        dedupedOpntionList = listDedup(optionList)
        dedupedSentenceList = hashableListDedup(jointedSentences)

        resList = []
        resList.extend(dedupedSentenceList)
        resList.extend(dedupedOpntionList)

        filePath = f"output/formatter/rxdata/{getCurrTimeInFmt("%y-%m-%d_%H-%M")}"
        fileName = filePath + "/allTextContent"
        self._exportListToJson(resList, f"{fileName}.json")

        resList = self._rmAllEscapes(resList)
        fileName += "_NoEscape"
        self._exportListToJson(resList, f"{fileName}.json")

        return resList