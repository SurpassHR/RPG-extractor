import os
from rubymarshal import reader
from rubymarshal.classes import RubyObject, UserDef
from typing import List, Any
from definitions import FileType, RubyObjAttrCode

from utils import printList, writeListToFile, traverseListBytesDecode, getFileListFromPath, listDedup
from ruby_obj_formatter import RubyObjFormatter

class Extractor(RubyObjFormatter):
    def __init__(self, extractPath: str) -> None:
        RubyObjFormatter.__init__(self)

        self.extractPath = extractPath
        self.rubyObjList: List[RubyObject] = []
        self.globalFirstWrite = True

        return

    def _readRxdata(self, filePath: str) -> List[RubyObject]:
        ret = []
        with open(filePath, 'rb') as f:
            data = reader.load(f)
            if isinstance(data, RubyObject):
                ret.append(data)
            elif isinstance(data, list):
                ret.append(data[1])
            pass

        return ret

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

    def procData(self):
        fileList = getFileListFromPath(self.extractPath, FileType.RXDATA)
        fileDataList = []
        for file in fileList:
            try:
                fileDataList.append(self._readRxdata(file))
                print(f'Succeed reading file {file}')
            except Exception as e:
                print(f'Error reading file {file}: {e}')
                continue

        for fileData in fileDataList:
            atomObjList: List[RubyObject] = []
            for rubyObj in fileData:
                try:
                    atomObjList = self._traverseRubyObj(rubyObj)
                except Exception as e:
                    print(f'Error processing RubyObject: {e}')
                    continue
            atomObjList = listDedup(atomObjList)
            printList(atomObjList, False)
            writeListToFile(atomObjList, 'debug_files/atomRubyObjs.txt', firstWrite=self.globalFirstWrite)
            self.globalFirstWrite = False
            self.rubyObjList.extend(atomObjList)

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
                if code == RubyObjAttrCode.TEXT_DISP:
                    textDisp = content[0].decode('utf-8') if isinstance(content[0], bytes) else content[0]
                    textDispList.append(textDisp)
                if code == RubyObjAttrCode.TITLE:
                    title = content[0].decode('utf-8') if isinstance(content[0], bytes) else content[0]
                    titleList.append(title)
                if code == RubyObjAttrCode.OPTION:
                    option = content[0]
                    if isinstance(content[0], list):
                        option = traverseListBytesDecode(option)
                    optionList.append(option)

        def __dedupDataListAndSaveDebugFile(dataList: list, fileName: str):
            printList(dataList, False)
            writeListToFile(dataList, fileName, firstWrite=True)

        # dialogueList = self.processRubyObjList(dialogueList)
        __dedupDataListAndSaveDebugFile(dialogueList, 'debug_files/dialogue.txt')
        __dedupDataListAndSaveDebugFile(optionList, 'debug_files/option.txt')

def testExtractRxdataInFolder(folderPath: str):
    extractor = Extractor(folderPath)
    extractor.procData()
    extractor.getDialogueFromRubyObjs()

if __name__ == '__main__':
    folderName = 'example_data'
    dataPath = os.path.join(os.getcwd(), folderName)
    testExtractRxdataInFolder(dataPath)