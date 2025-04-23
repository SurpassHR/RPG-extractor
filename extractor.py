import os
import sys
from pathlib import Path
from rubymarshal.classes import RubyObject, UserDef
from typing import List, Any

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from tools.readers.rubymarshal_reader.definitions import (
    FileExt,
    ReFileType,
    RubyObjAttrCode,
)
from tools.formatter import Formatter
from tools.exporter import Exporter
from tools.utils import (
    printList,
    writeListToFile,
    traverseListBytesDecode,
    hashableListDedup,
    listDedup,
    loadConfig
)
from tools.readers.rubymarshal_reader.rxdata_reader import RxdataReader
from tools.readers.folder_reader import getFilesInFolderByType

class Extractor:
    def __init__(self, gameDataFolder: str, outputDataFolder: str):
        self.gameDataFolder = gameDataFolder
        self.outputDataFolder = outputDataFolder
        self.rubyObjList: List[RubyObject] = []
        self.scriptsRxdata = []
        self.doodasRxdata: Any = None
        self.commonRxdata = []
        self.globalFirstWrite = True
        self.formatter = Formatter()
        self.exporter = Exporter()
        self.reader = RxdataReader()

    def _hasDeeperRubyObj(self, obj: RubyObject):
        rubyObjAttrs = obj.attributes
        return 'RubyObject' in str(rubyObjAttrs)

    def _traverseRubyObj(self, obj: RubyObject | Any) -> List[RubyObject]:
        if isinstance(obj, UserDef):
            return []

        retList = []

        def __extendRetList(extendData: list):
            if extendData is not None and extendData != []:
                retList.extend(extendData)

        def __procList(obj: list):
            # list需要保证每个进入递归的对象都是RubyObject
            for item in obj:
                res = self._traverseRubyObj(item)
                __extendRetList(res)
            printList(retList, False)
            return retList

        def __procDict(obj: dict):
            keys = obj.keys()
            for key in keys:
                res = self._traverseRubyObj(obj[key])
                __extendRetList(res)
            printList(retList, False)
            return retList

        def __procRubyObj(obj: RubyObject):
            if self._hasDeeperRubyObj(obj):
                attrs = obj.attributes
                res = self._traverseRubyObj(attrs)
                __extendRetList(res)
                printList(retList, False)
                return retList
            return [obj]

        # 可能是 list、dict或RubyObject
        if isinstance(obj, list):
            return __procList(obj)

        if isinstance(obj, dict):
            return __procDict(obj)

        if isinstance(obj, RubyObject):
            return __procRubyObj(obj)

        return retList

    def _readDataListFromFile(self, fileList: List[str]):
        for file in fileList:
            fileName = os.path.basename(file)
            try:
                self.reader.read(file)
                # print(f'Succeed reading file {fileName}')
            except Exception as e:
                print(f'Error reading file {fileName}: {e}')
                continue

        self.scriptsRxdata = self.reader.getRxdata(ReFileType.SCRIPTS)
        self.doodasRxdata = self.reader.getRxdata(ReFileType.DOODAS)
        self.commonRxdata = self.reader.getRxdata(ReFileType.COMMON)
        self.reader.clearRxdata()

    def _getAtomObjFromRubyObj(self, fileData) -> List[RubyObject]:
        atomObjList: List[RubyObject] = []
        if isinstance(fileData, RubyObject):
            atomObjList.extend(self._traverseRubyObj(fileData))
            return atomObjList
        for rubyObj in fileData:
            try:
                atomObjList.extend(self._traverseRubyObj(rubyObj))
            except Exception as e:
                print(f'Error processing RubyObject: {e}')
                continue

        return atomObjList

    def procData(self):
        fileList = getFilesInFolderByType(self.gameDataFolder, FileExt.RXDATA.value)
        self._readDataListFromFile(fileList)

        for fileData in self.commonRxdata:
            atomObjList: List[RubyObject] = self._getAtomObjFromRubyObj(fileData)
            atomObjList = listDedup(atomObjList)
            printList(atomObjList, False)
            writeListToFile(atomObjList, f'{self.outputDataFolder}/atomRubyObjs.txt', firstWrite=self.globalFirstWrite)
            self.globalFirstWrite = False
            self.rubyObjList.extend(atomObjList)

        self.exporter.exportToRb(list(self.scriptsRxdata), f'{self.outputDataFolder}/scripts.rb')
        self.exporter.exportToRb(self.doodasRxdata, f'{self.outputDataFolder}/doodas.rb')

    def getDialogueFromRubyObjs(self):
        textDispList = []
        titleList = []
        dialogueList = []
        optionList = []
        for item in self.rubyObjList:
            attrs = item.attributes
            code = attrs.get('@code')
            content: list = attrs.get('@parameters', [])
            if code:
                # 需要两者合并来展示完整对话
                if code == RubyObjAttrCode.TEXT_DISP or code == RubyObjAttrCode.TITLE:
                    dialogue = content[0].decode('utf-8') if isinstance(content[0], bytes) else content[0]
                    dialogueList.append(dialogue)
                elif code == RubyObjAttrCode.TEXT_DISP:
                    textDisp = content[0].decode('utf-8') if isinstance(content[0], bytes) else content[0]
                    textDispList.append(textDisp)
                elif code == RubyObjAttrCode.TITLE:
                    title = content[0].decode('utf-8') if isinstance(content[0], bytes) else content[0]
                    titleList.append(title)
                elif code == RubyObjAttrCode.OPTION:
                    option = content[0]
                    if isinstance(content[0], list):
                        option = traverseListBytesDecode(option)
                    optionList.append(option)

        def __SaveDebugFile(dataList: list, fileName: str):
            printList(dataList, False)
            writeListToFile(dataList, fileName, firstWrite=True)
            self.exporter.exportListToJson(dataList, fileName.split('.')[0] + '.json')

        dialogueList = self.formatter.sentenceJoint(dialogueList)
        dialogueList = hashableListDedup(dialogueList)
        __SaveDebugFile(dialogueList, f'{self.outputDataFolder}/dialogue.txt')
        optionList = listDedup(optionList)
        __SaveDebugFile(optionList, f'{self.outputDataFolder}/option.txt')

def testExtractRxdataInFolder():
    config = loadConfig()

    gameDataFolder = os.path.join(os.getcwd(), config.get('game_data_dir', 'example_data'))
    outputDataFolder = config.get('output_data_dir', 'debug_files')

    extractor = Extractor(gameDataFolder, outputDataFolder)
    extractor.procData()
    extractor.getDialogueFromRubyObjs()

if __name__ == '__main__':

    testExtractRxdataInFolder()