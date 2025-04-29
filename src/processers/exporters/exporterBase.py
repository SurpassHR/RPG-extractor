from typing import Any
from src.utils.autoRegister import AutoRegisterBase
from src.utils.fileTools import writeDictToJsonFile

class ExporterBase(AutoRegisterBase):
    def __init__(self, exportFolder: str):
        self.exportFolder = exportFolder

    def init(self):
        pass

    def _exportListToJson(self, data: list, exportJson: str) -> None:
        jsonContent: dict = {}
        for item in data:
            key = val = f'{item}'
            jsonContent[key] = val

        writeDictToJsonFile(jsonContent, exportJson, True)

    def export(self, data: Any) -> None:
        pass