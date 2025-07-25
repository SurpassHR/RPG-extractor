import os

from src.publicDef.levelDefs import LogLevels
from src.loggers.simpleLogger import loggerPrint
from src.processers.readers.readerBase import ReaderBase
from src.utils.fileTools import isFileExists
from src.utils.timeTools import getCurrTimeInFmt
from src.utils.decorators.execTimer import timer


class JsReader(ReaderBase):
    def __init__(self):
        super().__init__()

    @timer
    def read(self):
        super().read()

        targetFile = "plugins.js"
        for item in self.fileList:
            if targetFile in item:
                targetFile = item
                break

        if not isFileExists(targetFile):
            loggerPrint(
                f"Target file '{targetFile}' not in list.", level=LogLevels.WARNING
            )
            exit(-1)

        fd = open(targetFile, "r", encoding="utf-8")

        if fd:
            data = fd.read()
            debugFile = (
                f"output/reader/js/{getCurrTimeInFmt('%y-%m-%d_%H-%M')}/rawPlugins.js"
            )
            if os.path.exists(debugFile):
                os.remove(debugFile)
            if not os.path.exists(os.path.dirname(debugFile)):
                os.makedirs(os.path.dirname(debugFile))
            with open(debugFile, "a", encoding="utf-8") as f:
                f.write(data)
            return data
        else:
            loggerPrint(f"Read file {targetFile} err.")
            exit(-1)
