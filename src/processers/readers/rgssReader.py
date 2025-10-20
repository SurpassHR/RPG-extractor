# rgssReader 是 rubymarshallReader 的升级版

from typing import override
from src.publicDef.levelDefs import LogLevels
from src.loggers.simpleLogger import boldFont, loggerPrint
from src.processers.readers.readerBase import ReaderBase
from src.utils.decorators.execTimer import timer


class RgssReader(ReaderBase):
    def __init__(self):
        super().__init__()

    @timer
    @override
    def read(self) -> tuple[list, dict, list]:
        super().read()

        if not self.fileList:
            loggerPrint(f"File list is empty.", level=LogLevels.WARNING)
            exit(-1)

        return [], {}, []
