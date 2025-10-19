from typing import Any

from src.utils.configLoader import getConfig, setConfig
from src.publicDef.levelDefs import LogLevels
from src.loggers.simpleLogger import loggerPrint
from src.utils.autoRegister import AutoRegisterBase
from src.utils.decorators.execTimer import timer


class ReaderBase(AutoRegisterBase):
    def __init__(self):
        self.fileList = None

    def init(self, fileList: list[str]) -> None:
        self.fileList = fileList

    @timer
    def _load(self, filePath: str):
        loggerPrint(f"Loading file {filePath}.", level=LogLevels.DEBUG)

    def _setStageDataPath(self, path: str) -> None:
        setConfig("stage_data_path.read_stage", path)

    def _getStageDataPath(self) -> str:
        return getConfig("stage_data_path.read_stage")

    def read(self) -> Any:
        pass
