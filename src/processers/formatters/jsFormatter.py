import re
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from src.processers.formatters.formatterBase import FormatterBase
from src.utils.fileTools import writeListToFile
from src.utils.regexTools import execListMultiReSub, isMultiReFindall
from src.utils.timeTools import getCurrTimeInFmt

class JsFormatter(FormatterBase):
    def __init__(self):
        super().__init__()

    def _rmEscape(self, dataList: list) -> list:
        patternDict: dict[re.Pattern, str] = {
            re.compile(r'\\n[cr]*<\\c\[\d{1,3}\].*\\c>'): '',
            re.compile(r'\\\w\[\d{1,3}\]'): '\n',
            re.compile(r'\\c'): '\n',
            re.compile(r'\\\{'): '',
            re.compile(r'\\\}'): '',
            re.compile(r'\n{2,}'): '\n',
        }

        return execListMultiReSub(patternDict, dataList)

    def _rmDigit(self, dataList: list) -> list:
        subbedDataList: list[str] = []

        for item in dataList:
            if not isinstance(item, int):
                subbedDataList.append(item)

        patternDict: dict[re.Pattern, str] = {
            re.compile(r'^\d{1,}$'): '',
            re.compile(r'^-\d{1,}$'): '',
        }
        subbedDataList = execListMultiReSub(patternDict, subbedDataList)

        return subbedDataList

    def _rmBool(self, dataList: list) -> list:
        subbedDataList: list[str] = []

        for item in dataList:
            if not isinstance(item, bool):
                subbedDataList.append(item)

        patternDict: dict[re.Pattern, str] = {
            re.compile(r'true'): '',
            re.compile(r'false'): '',
        }
        subbedDataList = execListMultiReSub(patternDict, subbedDataList)

        return subbedDataList

    def _rmCode(self, dataList: list):
        patternList: list[re.Pattern[str]] = [
            re.compile(r'^[A-Z]{1}[a-z]+\(.+\)\.[A-Z|a-z]+'), # Axxx().Bxxx
            re.compile(r'^[A-Za-z]{1}[a-z]+\.[A-Z|a-z]+'), # Axxx.Bxxx[a-z]+\._*[A-za-z]+
            re.compile(r'[a-z]+\._*[A-Za-z]+'), # xxxx.yyyy
            re.compile(r'\$[A-Za-z]{1,}'), # $...
            re.compile(r'^%.*'), # %...
            re.compile(r'^[Ee][V|v]\d{3}(_[A-Za-z])*'), # evxxx...
            re.compile(r'^[A-Za-z]+[0-9]*_[A-Za-z]+'), # Axxx_Bxxx
            re.compile(r'[a-z]+[0-9]*_[a-z]+'), # axxx_bxxx
            re.compile(r'^_.*'), # _xxx
            re.compile(r'[A-Za-z0-9]+_$'), # xxx_
            re.compile(r'^[a-z][a-zA-Z0-9]*([A-Z][a-zA-Z0-9]*)*$'),  # 小驼峰
            re.compile(r'^[A-Z][a-zA-Z0-9]*([A-Z][a-zA-Z0-9]*)+$'),  # 大驼峰
            re.compile(r'#+.*'),
            re.compile(r'@+.*'),
            re.compile(r'%\d+')
        ]

        subbedDataList: list[str] = []
        for item in dataList:
            if not isMultiReFindall(patternList, item):
                subbedDataList.append(item)

        return subbedDataList

    def _rmUseless(self, dataList: list) -> list:
        patternList: list[re.Pattern[str]] = [
            re.compile(r'█+'),
            re.compile(r'={2,}'),
            re.compile(r'^-$'),
            re.compile('^\\n$'),
        ]

        subbedDataList: list[str] = []
        for item in dataList:
            if not isMultiReFindall(patternList, item):
                subbedDataList.append(item)

        return subbedDataList

    def format(self, data: list) -> list:
        resList = []

        fileName = f"output/formatter/js/{getCurrTimeInFmt('%y-%m-%d_%H-%M')}/pluginContent"

        resList = self._rmDigit(data)
        fileName += '_NoDigit'
        writeListToFile(
            resList,
            fileName + '.json'
        )

        resList = self._rmBool(resList)
        fileName += '_NoBool'
        writeListToFile(
            resList,
            fileName + '.json'
        )

        resList = self._rmCode(resList)
        fileName += '_NoCode'
        writeListToFile(
            resList,
            fileName + '.json'
        )

        resList = self._rmUseless(resList)
        fileName += '_NoUseless'
        writeListToFile(
            resList,
            fileName + '.json'
        )

        resList = self._rmEscape(resList)
        fileName += '_NoEscape'
        writeListToFile(
            resList,
            fileName + '.json'
        )

        return resList

if __name__ == '__main__':
    fmter = JsFormatter()
    dataList = [
        "\"I'll put every detail of this journey as a diary in my\nresearch log, so I can keep track of things during my\nstay.\" \n\\}-\\c[17]Sasha Stewart.\\c",
    ]
    res = fmter.format(dataList)
