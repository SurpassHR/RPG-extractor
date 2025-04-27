from typing import Any

from src.loggers.simpleLogger import loggerPrint, loggerPrintList
from src.utils.autoRegister import AutoRegisterBase
from src.utils.decorators.execTimer import execTimer

class ReaderBase(AutoRegisterBase):
    def __init__(self):
        pass

    def init(self, fileList: list[str]) -> None:
        self.fileList = fileList

    @execTimer
    def _load(self):
        loggerPrint(f"Loading file list:")
        loggerPrintList(self.fileList)

    def read(self) -> Any:
        self._load()