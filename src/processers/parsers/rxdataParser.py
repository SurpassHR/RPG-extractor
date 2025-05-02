from typing import Any
from rubymarshal.classes import RubyObject

from src.loggers.simpleLogger import loggerPrintList
from src.processers.parsers.parserBase import ParserBase
from src.utils.dataStructTools import getAtomObjFromRubyObj, listDedup
from src.utils.fileTools import writeListToFile, writeListToRubyFile
from src.utils.timeTools import getCurrTimeInFmt
from src.utils.decorators.execTimer import timer

class RxdataParser(ParserBase):
    def __init__(self):
        super().__init__()
        self.rubyObjList: list = []

    @timer
    def parse(self, data: tuple[list, dict, list]) -> Any:
        scriptsRxdata, doodadsRxdata, commonRxdata = data
        filePath = f"output/parser/rxdata/{getCurrTimeInFmt("%y-%m-%d_%H-%M")}"
        for i, fileData in enumerate(commonRxdata):
            atomObjList: list[RubyObject] = getAtomObjFromRubyObj(fileData)
            atomObjList = listDedup(atomObjList)
            # loggerPrintList(atomObjList)
            writeListToFile(atomObjList, f'{filePath}/atomRubyObjs.txt', firstWrite=(i == 0))
            self.globalFirstWrite = False
            self.rubyObjList.extend(atomObjList)

        writeListToRubyFile(list(scriptsRxdata), f'{filePath}/scriptsRxdata.rb')
        writeListToRubyFile([doodadsRxdata], f'{filePath}/doodadsRxdata.rb')