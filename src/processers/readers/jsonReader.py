from src.processers.readers.readerBase import ReaderBase
from src.loggers.simpleLogger import loggerPrint, loggerPrintList
from src.publicDef.levelDefs import LogLevels
from src.utils.fileTools import readJson
from src.utils.decorators.execTimer import execTimer

class JsonReader(ReaderBase):
    def __init__(self, fileList: list[str]):
        super().__init__(fileList)
        self._load()

        self.jsonData: list = []

    @execTimer
    def _load(self):
        loggerPrint(f"Loading file list:")
        loggerPrintList(self.fileList)

    @execTimer
    def read(self):
        loggerPrint(f"Call JsonReader.read().", level=LogLevels.DEBUG)
        jsonData: list = []
        for file in self.fileList:
            jsonData.append(readJson(file))

        # loggerPrintList(jsonData)

    def get(self):
        pass