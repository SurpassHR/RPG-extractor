import os

from src.processers.exporters.exporterBase import ExporterBase
from src.utils.timeTools import getCurrTimeInFmt
from src.utils.decorators.execTimer import timer

class RxdataExporter(ExporterBase):
    def __init__(self, exportFolder: str):
        super().__init__(exportFolder)

    @timer
    def export(self, data: list) -> None:
        path = os.path.join(self.exportFolder, 'rxdataExport', f"{getCurrTimeInFmt('%y-%m-%d_%H-%M')}.json")
        self._exportListToJson(data, path)