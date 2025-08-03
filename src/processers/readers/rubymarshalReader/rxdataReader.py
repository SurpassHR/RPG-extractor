import os
from typing import Any
from rubymarshal.classes import RubyObject

from src.loggers.simpleLogger import loggerPrint
from src.processers.readers.rubymarshalReader.rubymarshalDecoder import (
    RubyMarshalDecoder,
)
from src.publicDef.levelDefs import LogLevels
from src.processers.readers.readerBase import ReaderBase
from src.utils.fileTools import getFileName, writeListToFile, writeListToRubyFile
from src.utils.dataStructTools import (
    getAtomObjFromRubyObj,
    listDedup,
    traverseListBytesDecode,
)
from src.utils.decorators.execTimer import timer
from src.utils.timeTools import getCurrTimeInFmt


class RxdataReader(ReaderBase):
    def __init__(self):
        super().__init__()  # 将str转换为list[str]以匹配父类签名

        self.scriptsRxdata: list = []
        self.doodadsRxdata: Any = None
        self.commonRxdata: list = []

        self.commonDataFirstWrite: bool = True

    def _readCommonRxdata(self, filePath: str) -> list[RubyObject]:
        data = self._load(filePath)

        ret = []
        if isinstance(data, RubyObject):
            ret.append(data)
        elif isinstance(data, list):
            ret.append(data[1])

        return ret

    def _readScriptsRxdata(self, filePath: str) -> list[RubyObject]:
        data = self._load(filePath)
        ret = traverseListBytesDecode(data)
        return ret

    def _readDoodasRxdata(self, filePath: str):
        # binary mode doesn't take an encoding argument
        f = open(filePath, "rb")
        return f.read().decode()

    def _readOutAndSave(self, filePath: str):
        baseName = getFileName(filePath)
        if baseName == "Scripts.rxdata":
            self.scriptsRxdata.extend(self._readScriptsRxdata(filePath))
        elif "doodads.rxdata" in baseName:
            self.doodadsRxdata = self._readDoodasRxdata(filePath)
        else:
            self.commonRxdata.extend(self._readCommonRxdata(filePath))

    def _load(self, filePath: str):
        # binary mode doesn't take an encoding argument
        fd = open(filePath, "rb")
        if fd.read(1) != b"\x04":
            raise ValueError(r"Expected token \x04")
        if fd.read(1) != b"\x08":
            raise ValueError(r"Expected token \x08")

        loader = RubyMarshalDecoder(fd, None)
        return loader.read()

    @timer
    def read(self) -> tuple[list, dict, list]:
        for file in self.fileList:
            try:
                self._readOutAndSave(file)
            except Exception as e:
                loggerPrint(f"Error reading file {file}: {e}", level=LogLevels.ERROR)
                continue

        outputBaseFolder = os.path.join("output", "reader", "rxdata", getCurrTimeInFmt("%y-%m-%d_%H-%M"))
        for fileData in self.commonRxdata:
            atomObjList: list[RubyObject] = getAtomObjFromRubyObj(fileData)
            atomObjList = listDedup(atomObjList)
            # loggerPrintList(atomObjList)
            writeListToFile(
                dataList=atomObjList,
                fileName=os.path.join(outputBaseFolder, "commonRxdata.txt"),
                firstWrite=self.commonDataFirstWrite,
            )
            self.commonDataFirstWrite = False

        writeListToRubyFile(
            dataList=list(self.scriptsRxdata),
            fileName=os.path.join(outputBaseFolder, "scriptsRxdata.rb"),
        )
        writeListToRubyFile(
            dataList=[self.doodadsRxdata],
            fileName=os.path.join(outputBaseFolder, "doodadsRxdata.rb"),
        )

        return (self.scriptsRxdata, self.doodadsRxdata, self.commonRxdata)
