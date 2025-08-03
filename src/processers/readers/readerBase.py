from typing import Any

from src.publicDef.levelDefs import LogLevels
from src.loggers.simpleLogger import loggerPrint
from src.utils.autoRegister import AutoRegisterBase
from src.utils.decorators.execTimer import timer


class ReaderBase(AutoRegisterBase):
    def __init__(self):
        pass

    def init(self, fileList: list[str]) -> None:
        self.fileList = fileList

    @timer
    def _load(self, filePath: str):
        loggerPrint(f"Loading file {filePath}.", level=LogLevels.DEBUG)

    def read(self) -> Any:
        pass
