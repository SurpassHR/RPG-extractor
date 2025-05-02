from typing import Any
from src.utils.autoRegister import AutoRegisterBase
from src.utils.fileTools import FileTool

class ExporterBase(AutoRegisterBase, FileTool):
    def __init__(self, exportFolder: str):
        self.exportFolder = exportFolder

    def init(self):
        pass

    def export(self, data: Any) -> None:
        pass