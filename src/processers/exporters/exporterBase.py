from typing import Any
from src.utils.autoRegister import AutoRegisterBase
from src.utils.fileTools import FileTool


class ExporterBase(AutoRegisterBase, FileTool):
    def __init__(self, exportFolder: str, title: str = ""):
        self.exportFolder = exportFolder
        self.title = title

    def init(self):
        pass

    def export(self, data: Any) -> None:
        pass
