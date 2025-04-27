from src.processers.readers.readerBase import ReaderBase
from src.loggers.simpleLogger import loggerPrint
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
    def read(self) -> dict:
        super().read()
        jsonData = {}
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