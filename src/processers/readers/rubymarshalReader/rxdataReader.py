
import zlib
from typing import Any
from rubymarshal.classes import RubyObject, RubyString

from src.loggers.simpleLogger import loggerPrint
from src.processers.readers.rubymarshalReader.rubymarshalDecoder import RubyMarshalDecoder
from src.publicDef.levelDefs import LogLevels
from src.processers.readers.readerBase import ReaderBase
from src.utils.fileTools import getFileName

class RxdataReader(ReaderBase):
    def __init__(self):
        super().__init__()  # 将str转换为list[str]以匹配父类签名

        self.scriptsRxdata: list = []
        self.doodasRxdata: Any = None
        self.commonRxdata: list = []

    def _readCommonRxdata(self, filePath: str) -> list[RubyObject]:
        data = self._load(filePath)

        ret = []
        if isinstance(data, RubyObject):
            ret.append(data)
        elif isinstance(data, list):
            ret.append(data[1])

        return ret

    def _traverseListBytesDecode(self, dataList: list) -> list:
        def __decode(item) -> str:
            try:
                item = item.decode('utf-8')
            except:
                item = zlib.decompress(item).decode('utf-8')
            return item

        retList = []
        for item in dataList:
            if isinstance(item, list):
                retList.extend(self._traverseListBytesDecode(item))
                continue
            if isinstance(item, str):
                retList.append(item)
                continue
            if isinstance(item, RubyString):
                retList.append(item.text)
                continue
            if isinstance(item, bytes):
                item = __decode(item)
                retList.append(item)
                continue

        return retList

    def _readScriptsRxdata(self, filePath: str) -> list[RubyObject]:
        data = self._load(filePath)
        ret = self._traverseListBytesDecode(data)
        return ret

    def _readDoodasRxdata(self, filePath: str):
        f = open(filePath, 'rb')
        return f.read().decode()

    def _readOutAndSave(self, filePath: str):
        baseName = getFileName(filePath)
        if baseName == 'Scripts.rxdata':
            self.scriptsRxdata.extend(self._readScriptsRxdata(filePath))
        elif 'doodads.rxdata' in baseName:
            self.doodasRxdata = self._readDoodasRxdata(filePath)
        else:
            self.commonRxdata.extend(self._readCommonRxdata(filePath))

    def _load(self, filePath: str):
        fd = open(filePath, 'rb')
        if fd.read(1) != b"\x04":
            raise ValueError(r"Expected token \x04")
        if fd.read(1) != b"\x08":
            raise ValueError(r"Expected token \x08")

        loader = RubyMarshalDecoder(fd, None)
        return loader.read()

    def read(self) -> tuple[list, dict, list]:
        for file in self.fileList:
            try:
                self._readOutAndSave(file)
            except Exception as e:
                loggerPrint(f'Error reading file {file}: {e}', level=LogLevels.ERROR)
                continue
        return (
            self.scriptsRxdata,
            self.doodasRxdata,
            self.commonRxdata
        )