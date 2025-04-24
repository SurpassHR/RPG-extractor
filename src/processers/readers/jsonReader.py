from src.processers.readers.readerBase import ReaderBase
from src.loggers.simpleLogger import loggerPrint, printList

class JsonReader(ReaderBase):
    def __init__(self, fileList: list[str]):
        super().__init__(fileList)
        self._load()

    def _load(self):
        loggerPrint(f"Loading file list:")
        printList(self.fileList)