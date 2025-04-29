from src.processers.exporters.exporterBase import ExporterBase

class RxdataExporter(ExporterBase):
    def __init__(self, exportFolder: str):
        super().__init__(exportFolder)