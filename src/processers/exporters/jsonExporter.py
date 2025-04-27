import os
from src.processers.exporters.exporterBase import ExporterBase
from src.utils.timeTools import getCurrTimeInFmt
from src.utils.fileTools import writeDictToJsonFile

class JsonExporter(ExporterBase):
    def __init__(self, exportFolder: str):
        super().__init__(exportFolder)

    def _exportListToJson(self, data: list, exportJson: str):
        jsonContent: dict = {}
        for item in data:
            key = val = f'{item}'
            jsonContent[key] = val

        writeDictToJsonFile(jsonContent, exportJson, True)

    def export(self, data: list) -> None:
        path = os.path.join(self.exportFolder, f"{getCurrTimeInFmt('%y-%m-%d_%H-%M')}.json")
        self._exportListToJson(data, path)
