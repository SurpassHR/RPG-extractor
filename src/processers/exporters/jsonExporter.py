import os
from typing import Any

from src.processers.exporters.exporterBase import ExporterBase
from src.utils.timeTools import getCurrTimeInFmt


class JsonExporter(ExporterBase):
    def init(self, exportFolder: str, title: str = ""):
        super().init(exportFolder=exportFolder, title=title)

    def export(self, data: list[Any]) -> None:
        path = os.path.join(
            self.exportFolder,
            "jsonExport" if self.title == "" else self.title,
            f"{getCurrTimeInFmt('%y-%m-%d_%H-%M')}.json",
        )
        self._exportListToJson(data, path)
