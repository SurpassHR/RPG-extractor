import os
import threading
import queue
from rubymarshal import reader
from rubymarshal.classes import RubyObject, UserDef
from typing import List, Any
from definitions import FileType, RubyObjAttrCode

from utils import printList, writeListToFile, traverseListBytesDecode, getFileListFromPath, listDedup

class Extractor:
    def __init__(self, extractPath: str):
        self.extractPath = extractPath
        self.rubyObjList: List[RubyObject] = []
        self.dataQueue = queue.Queue()

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

        def __procFile(file: str, fileDataList: list):
            try:
                fileDataList.append(self._readRxdata(file))
                print(f'Succeed reading file {file}')
            except Exception as e:
                print(f'Error reading file {file}: {e}')

        readFileThreads: List[threading.Thread] = []
        for file in fileList:
            thread = threading.Thread(target=__procFile, args=(file, fileDataList))
            readFileThreads.append(thread)
            thread.start()

        for thread in readFileThreads:
            thread.join()

        # 多线程处理数据，写入队列
        processThreads: List[threading.Thread] = []
        for fileData in fileDataList:
            def __processAndQueue(data):
                atomObjList: List[RubyObject] = []
                for rubyObj in data:
                    try:
                        atomObjList.extend(self._traverseRubyObj(rubyObj))
                    except Exception as e:
                        print(f'Error processing RubyObject: {e}')
                        continue
                self.dataQueue.put(atomObjList) # 数据放入队列

            thread = threading.Thread(target=__processAndQueue, args=(fileData,))
            processThreads.append(thread)
            thread.start()

        for thread in processThreads:
            thread.join()

        # 单线程写入文件
        def __writeToFile(file_name, data_queue):
            first_write = True
            while not data_queue.empty():
                data = data_queue.get()
                writeListToFile(data, file_name, first_write)
                first_write = False

        # 将所有结果合并到 self.rubyObjList
        while not self.dataQueue.empty():
            self.rubyObjList.extend(self.dataQueue.get())

        writeThread = threading.Thread(target=__writeToFile, args=('debug_files/atomRubyObjs.txt', self.dataQueue))
        writeThread.start()
        writeThread.join()

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
            # 去重时使用列表推理，而不是转为set再转回list，保证对话顺序不变
            tempDataList = listDedup(dataList)
            printList(tempDataList, False)
            writeListToFile(tempDataList, fileName, firstWrite=True)

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