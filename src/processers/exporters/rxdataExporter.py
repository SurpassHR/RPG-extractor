import os

from src.processers.exporters.exporterBase import ExporterBase
from src.utils.timeTools import getCurrTimeInFmt
from src.utils.decorators.execTimer import timer


class RxdataExporter(ExporterBase):
    def __init__(self, exportFolder: str, title: str = ""):
        super().__init__(exportFolder=exportFolder, title=title)

    @timer
    def export(self, data: list) -> None:
        path = os.path.join(
            self.exportFolder,
            "rxdataExport" if self.title == "" else self.title,
            f"{getCurrTimeInFmt('%y-%m-%d_%H-%M')}.json",
        )
        self._exportListToJson(data, path)
