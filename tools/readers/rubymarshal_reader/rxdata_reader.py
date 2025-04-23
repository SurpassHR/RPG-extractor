
import sys
from pathlib import Path
from io import BufferedReader
from typing import Any
from rubymarshal.classes import RubyObject

sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent))

from tools.utils import traverseListBytesDecode
from tools.public_def.reader_defs import FileExt
from tools.public_def.level_defs import LogLevels
from tools.readers.reader_base import ReaderBase
from tools.readers.rubymarshal_reader.rubymarshal_decoder import RubyMarshalDecoder
from tools.readers.reader_utils import (
    getFileName,
)
from tools.loggers.simple_logger import loggerPrint

class RxdataReader(ReaderBase):
    def __init__(self, fileList: list[str]) -> None:
        self.scriptsRxdata: list = []
        self.doodasRxdata: Any = None
        self.commonRxdata: list = []

        super().__init__(fileList, FileExt.RXDATA)

    def _load(self, fd: BufferedReader, registry = None):
        if fd.read(1) != b"\x04":
            raise ValueError(r"Expected token \x04")
        if fd.read(1) != b"\x08":
            raise ValueError(r"Expected token \x08")

        loader = RubyMarshalDecoder(fd, registry)
        return loader.read()

    def _readCommonRxdata(self, filePath: str) -> list[RubyObject]:
        data = self._load(open(filePath, 'rb'))

        ret = []
        if isinstance(data, RubyObject):
            ret.append(data)
        elif isinstance(data, list):
            ret.append(data[1])

        return ret

    def _readScriptsRxdata(self, filePath: str) -> list[RubyObject]:
        data = self._load(open(filePath, 'rb'))
        ret = traverseListBytesDecode(data)
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

    def _readDataListFromFile(self, fileList: list[str]):
        for file in fileList:
            try:
                self._readOutAndSave(file)
            except Exception as e:
                loggerPrint(f'Error reading file {file}: {e}', level=LogLevels.ERROR)
                continue

    def read(self) -> None:
        self._readDataListFromFile(self.fileList)

    def getData(self) -> tuple[list, dict, list]:
        return (
            self.scriptsRxdata,
            self.doodasRxdata,
            self.commonRxdata
        )