
import sys
from pathlib import Path
from io import BufferedReader
from typing import List, Tuple, Any
from rubymarshal.classes import RubyObject

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from tools.utils import (
    traverseListBytesDecode,
)
from tools.readers.rubymarshal_reader.definitions import ReFileType
from tools.readers.rubymarshal_reader.reader_base import ReaderBase
from tools.readers.rubymarshal_reader.ruby_marshal_decoder import RubyMarshalDecoder
from tools.readers.reader_utils import (
    getFileName,
)

class RxdataReader(ReaderBase):
    def __init__(self) -> None:
        self.scriptsRxdata: list = []
        self.doodasRxdata: Any = None
        self.commonRxdata: list = []
        super().__init__(file_path='')

    def _load(self, fd: BufferedReader, registry = None):
        if fd.read(1) != b"\x04":
            raise ValueError(r"Expected token \x04")
        if fd.read(1) != b"\x08":
            raise ValueError(r"Expected token \x08")

        loader = RubyMarshalDecoder(fd, registry)
        return loader.read()

    def _readCommonRxdata(self, filePath: str) -> List[RubyObject]:
        data = self._load(open(filePath, 'rb'))

        ret = []
        if isinstance(data, RubyObject):
            ret.append(data)
        elif isinstance(data, list):
            ret.append(data[1])

        return ret

    def _readScriptsRxdata(self, filePath: str) -> List[RubyObject]:
        data = self._load(open(filePath, 'rb'))
        ret = traverseListBytesDecode(data)
        return ret

    def _readDoodasRxdata(self, filePath: str):
        f = open(filePath, 'rb')
        return f.read().decode()

    def read(self, filePath: str):
        baseName = getFileName(filePath)
        if baseName == 'Scripts.rxdata':
            self.scriptsRxdata.extend(self._readScriptsRxdata(filePath))
        elif 'doodads.rxdata' in baseName:
            self.doodasRxdata = self._readDoodasRxdata(filePath)
        else:
            self.commonRxdata.extend(self._readCommonRxdata(filePath))

    def getRxdata(self, dataType: ReFileType = ReFileType.ALL) -> list | dict:
        if dataType == ReFileType.SCRIPTS:
            return self.scriptsRxdata.copy()
        elif dataType == ReFileType.DOODAS:
            return self.doodasRxdata
        elif dataType == ReFileType.COMMON:
            return self.commonRxdata.copy()
        return []

    def getAllRxdata(self) -> Tuple[list, dict, list]:
        return (
            self.scriptsRxdata,
            self.doodasRxdata,
            self.commonRxdata
        )

    def clearRxdata(self, dataType: ReFileType = ReFileType.ALL):
        if dataType == ReFileType.SCRIPTS:
            self.scriptsRxdata.clear()
        elif dataType == ReFileType.COMMON:
            self.commonRxdata.clear()
        else:
            self.scriptsRxdata.clear()
            self.commonRxdata.clear()