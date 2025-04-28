import os

from src.processers.exporters.exporterBase import ExporterBase
from src.utils.timeTools import getCurrTimeInFmt

class JsExporter(ExporterBase):
    def __init__(self, exportFolder):
        super().__init__(exportFolder)

    def export(self, data: list) -> None:
        path = os.path.join(self.exportFolder, 'jsExport', f"{getCurrTimeInFmt('%y-%m-%d_%H-%M')}.json")
        self._exportListToJson(data, path)