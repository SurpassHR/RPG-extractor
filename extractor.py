import os
from enum import StrEnum, IntEnum
from rubymarshal import reader
from rubymarshal.classes import RubyObject, UserDef
from typing import List, Any
from utils import printList, writeListToFile, traverseListBytesDecode

class FileType(StrEnum):
    RXDATA = '.rxdata'
    RVDATA = '.rvdata'

class RubyObjAttrCode(IntEnum):
    TITLE = 101 # 标题
    OPTION = 102 # 选项
    TEXT_DISP = 401 # 文本显示

class Extractor:
    def __init__(self, extractPath: str):
        self.extractPath = extractPath
        self.rubyObjList: List[RubyObject] = []

    def _getFileList(self, extractPath: str, fileType: FileType):
        fileExt = fileType.value
        fileList = os.listdir(extractPath)
        fileList = [file for file in fileList if os.path.splitext(file)[1] == fileExt]
        fileList = [os.path.join(extractPath, file) for file in fileList]
        return fileList

    def _readRxdata(self, filePath: str) -> List[RubyObject]:
        ret = []
        print(filePath)
        with open(filePath, 'rb') as f:
            data = reader.load(f)
            if isinstance(data, RubyObject):
                ret.append(data)
            elif isinstance(data, list):
                ret.append(data[1])
            pass
        return ret

    def _readRvdata(self, filePath: str):
        pass

    def _hasDeeperRubyObj(self, obj: RubyObject):
        rubyObjAttrs = obj.attributes
        return 'RubyObject' in str(rubyObjAttrs)

    def _traverseRubyObj(self, obj: RubyObject | Any) -> List[RubyObject]:
        if isinstance(obj, UserDef):
            return []

        retList = []

        def __extendRetList(extendData: list):
            if res is not None and res != []:
                retList.extend(extendData)

        # 可能是 list、dict或RubyObject
        if isinstance(obj, list):
            # list需要保证每个进入递归的对象都是RubyObject
            for item in obj:
                res = self._traverseRubyObj(item)
                __extendRetList(res)
            printList(retList, False)
            return retList

        if isinstance(obj, dict):
            keys = obj.keys()
            for key in keys:
                try:
                    res = self._traverseRubyObj(obj[key])
                    __extendRetList(res)
                except:
                    continue
            printList(retList, False)
            return retList

        if isinstance(obj, RubyObject):
            if self._hasDeeperRubyObj(obj):
                attrs = obj.attributes
                res = self._traverseRubyObj(attrs)
                __extendRetList(res)
                printList(retList, False)
                return retList
            return [obj]

        return retList

    def procData(self):
        fileList = self._getFileList(self.extractPath, FileType.RXDATA)
        fileDataList = []
        for file in fileList:
            try:
                fileDataList.append(self._readRxdata(file))
            except:
                continue

        for fileData in fileDataList:
            for rubyObj in fileData:
                atomObjList = self._traverseRubyObj(rubyObj)
            printList(atomObjList, False)
            writeListToFile(atomObjList, 'debug_files/atomRubyObjs.txt')
            self.rubyObjList.extend(atomObjList)

    def getDialogueFromRubyObjs(self):
        textDispList = []
        titleList = []
        optionList = []
        for item in self.rubyObjList:
            attrs = item.attributes
            code = attrs.get('@code')
            content = attrs.get('@parameters')
            if code:
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

        # 去重
        textDispList = list(set(textDispList))
        printList(textDispList, True)
        writeListToFile(textDispList, 'debug_files/textDisp.txt')

        # 去重
        titleList = list(set(titleList))
        printList(titleList, True)
        writeListToFile(titleList, 'debug_files/title.txt')

        # 去重
        tempOptionList = []
        [item for item in optionList if item not in tempOptionList]
        printList(tempOptionList, True)
        writeListToFile(tempOptionList, 'debug_files/option.txt')

class FileExtractor(Extractor):
    def __init__(self, extractPath):
        super().__init__(extractPath)

    def _getFileList(self, extractPath, fileType):
        if os.path.exists(self.extractPath):
            absPath = os.path.join(os.getcwd(), self.extractPath)
            return [absPath]

def testExtractRxdataInFolder(folderPath: str):
    extractor = Extractor(folderPath)
    extractor.procData()
    extractor.getDialogueFromRubyObjs()

def testExtractRxdataFromFile(filePath: str):
    extractor = FileExtractor(filePath)
    extractor.procData()
    extractor.getDialogueFromRubyObjs()

if __name__ == '__main__':
    folderName = 'example_data'
    dataPath = os.path.join(os.getcwd(), folderName)
    testExtractRxdataInFolder(dataPath)

    # filePath = os.path.join('example_data', 'Scripts.rxdata')
    # testExtractRxdataFromFile(filePath)