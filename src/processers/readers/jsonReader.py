from rich.progress import track

from src.processers.readers.readerBase import ReaderBase
from src.loggers.simpleLogger import loggerPrint
from src.utils.fileTools import getFileNameWithoutExt, readJson, writeDictToJsonFile
from src.utils.decorators.execTimer import timer
from src.utils.timeTools import getCurrTimeInFmt


class JsonReader(ReaderBase):
    def __init__(self):
        super().__init__()

    @timer
    def read(self) -> dict:
        super().read()

        jsonData = {}
        for file in track((self.fileList), description="Reading files..."):
            data = readJson(file)
            fileNameWithoutExt = getFileNameWithoutExt(file)
            jsonData[fileNameWithoutExt] = data
            self._setStageDataPath(f"output/reader/json/{getCurrTimeInFmt('%y-%m-%d_%H-%M')}/{fileNameWithoutExt}.json")
            writeDictToJsonFile(data, self._getStageDataPath())
        loggerPrint(f"Read data type '{type(jsonData)}'")

        return jsonData
