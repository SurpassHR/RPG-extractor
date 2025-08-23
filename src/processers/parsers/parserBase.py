from typing import Any

from src.utils.configLoader import getConfig, setConfig
from src.utils.autoRegister import AutoRegisterBase


class ParserBase(AutoRegisterBase):
    def __init__(self):
        pass

    def _setStageDataPath(self, path: str):
        setConfig("stage_data_path.parse_stage", path)

    def _getStageDataPath(self) -> str:
        return getConfig("stage_data_path.parse_stage")

    def init(self):
        pass

    def parse(self, data: Any) -> Any:
        pass
