from rubymarshal.classes import RubyObject
from rich.progress import track

from src.publicDef.readerDefs import RubyObjAttrCode
from src.processers.parsers.parserBase import ParserBase
from src.utils.dataStructTools import getAtomObjFromRubyObj, listDedup, traverseListBytesDecode
from src.utils.fileTools import writeListToFile, writeListToRubyFile
from src.utils.timeTools import getCurrTimeInFmt
from src.utils.decorators.execTimer import timer


class RxdataParser(ParserBase):
    def __init__(self):
        super().__init__()

    def _parseToGetAtomRubyObj(self, data, filePath: str):
        rubyObjList: list = []
        for i, fileData in track(enumerate(data), description="Parsing to get atom RubyObjects..."):
            atomObjList: list[RubyObject] = getAtomObjFromRubyObj(fileData)
            atomObjList = listDedup(atomObjList)
            # loggerPrintList(atomObjList)
            writeListToFile(atomObjList, filePath, firstWrite=(i == 0))
            rubyObjList.extend(atomObjList)

        return rubyObjList

    def _parseToGetDialogueFromRubyObjs(self, rubyObjList) -> tuple[list, list]:
        textDispList = []
        titleList = []
        dialogueList = []
        optionList = []
        for item in track(rubyObjList, description="Parsing to get dialogue data..."):
            attrs = item.attributes
            code = attrs.get("@code")
            content: list = attrs.get("@parameters", [])
            if code:
                # 需要两者合并来展示完整对话
                if code == RubyObjAttrCode.TEXT_DISP or code == RubyObjAttrCode.TITLE:
                    dialogue = content[0].decode("utf-8") if isinstance(content[0], bytes) else content[0]
                    dialogueList.append(dialogue)
                elif code == RubyObjAttrCode.TEXT_DISP:
                    textDisp = content[0].decode("utf-8") if isinstance(content[0], bytes) else content[0]
                    textDispList.append(textDisp)
                elif code == RubyObjAttrCode.TITLE:
                    title = content[0].decode("utf-8") if isinstance(content[0], bytes) else content[0]
                    titleList.append(title)
                elif code == RubyObjAttrCode.OPTION:
                    option = content[0]
                    if isinstance(content[0], list):
                        option = traverseListBytesDecode(option)
                    optionList.append(option)

        return dialogueList, optionList

    @timer
    def parse(self, data: tuple[list, dict, list]) -> tuple[list, list]:
        scriptsRxdata, doodadsRxdata, commonRxdata = data
        filePath = f"output/parser/rxdata/{getCurrTimeInFmt('%y-%m-%d_%H-%M')}"
        writeListToRubyFile(list(scriptsRxdata), f"{filePath}/scriptsRxdata.rb")
        writeListToRubyFile([doodadsRxdata], f"{filePath}/doodadsRxdata.rb")
        rubyObjList = self._parseToGetAtomRubyObj(commonRxdata, f"{filePath}/atomRubyObjs.txt")
        return self._parseToGetDialogueFromRubyObjs(rubyObjList)
