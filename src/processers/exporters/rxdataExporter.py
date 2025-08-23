import os

from src.processers.exporters.exporterBase import ExporterBase
from src.utils.timeTools import getCurrTimeInFmt
from src.utils.decorators.execTimer import timer


class RxdataExporter(ExporterBase):
    def init(self, exportFolder: str, title: str = ""):
        return super().init(exportFolder, title)

    @timer
    def export(self, data: list) -> None:
        path = os.path.join(
            self.exportFolder,
            "rxdataExport" if self.title == "" else self.title,
            f"{getCurrTimeInFmt('%y-%m-%d_%H-%M')}.json",
        )
        self._exportListToJson(data, path)
