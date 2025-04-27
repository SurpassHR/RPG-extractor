from typing import Any
from src.utils.autoRegister import AutoRegisterBase

class ExporterBase(AutoRegisterBase):
    def __init__(self, exportFolder: str):
        self.exportFolder = exportFolder

    def init(self):
        pass

    def export(self, data: Any) -> None:
        pass