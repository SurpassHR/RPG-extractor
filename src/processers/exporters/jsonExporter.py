import os
from src.processers.exporters.exporterBase import ExporterBase
from src.utils.timeTools import getCurrTimeInFmt


class JsonExporter(ExporterBase):
    def __init__(self, exportFolder: str, title: str = ""):
        super().__init__(exportFolder=exportFolder, title=title)

    def export(self, data: list) -> None:
        path = os.path.join(self.exportFolder, "jsonExport", f"{getCurrTimeInFmt('%y-%m-%d_%H-%M')}.json")
        self._exportListToJson(data, path)
