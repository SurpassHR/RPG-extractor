import os

from src.processers.exporters.exporterBase import ExporterBase
from src.utils.timeTools import getCurrTimeInFmt


class JsExporter(ExporterBase):
    def init(self, exportFolder: str, title: str = ""):
        return super().init(exportFolder, title)

    def export(self, data: list) -> None:
        path = os.path.join(
            self.exportFolder,
            "jsExport" if self.title == "" else self.title,
            f"{getCurrTimeInFmt('%y-%m-%d_%H-%M')}.json",
        )
        self._exportListToJson(data, path)
