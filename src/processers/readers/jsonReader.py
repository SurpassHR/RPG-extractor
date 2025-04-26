from src.processers.readers.readerBase import ReaderBase
from src.loggers.simpleLogger import loggerPrint, loggerPrintList
from src.publicDef.levelDefs import LogLevels
from src.utils.fileTools import (
    getFileNameWithoutExt,
    readJson,
    writeDictToJsonFile
)
from src.utils.decorators.execTimer import execTimer
from src.utils.timeTools import getCurrTimeInFmt

class JsonReader(ReaderBase):
    def __init__(self):
        super().__init__()

    @execTimer
    def _load(self):
        loggerPrint(f"Loading file list:")
        loggerPrintList(self.fileList)

    @execTimer
    def read(self) -> dict:
        self._load()
        loggerPrint(f"Call JsonReader.read().", level=LogLevels.DEBUG)
        jsonData: dict[str, list] = {}
        for file in self.fileList:
            data = readJson(file)
            fileNameWithoutExt = getFileNameWithoutExt(file)
            jsonData[fileNameWithoutExt] = data
            writeDictToJsonFile(
                data,
                f"output/reader/json/{getCurrTimeInFmt('%y-%m-%d_%H-%M')}/{fileNameWithoutExt}.json"
            )
        loggerPrint(f"Read data type '{type(jsonData)}'")

        return jsonData