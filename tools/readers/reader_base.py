import sys
from pathlib import Path
from typing import Any
from io import BufferedReader

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from tools.public_def.reader_defs import FileExt
from tools.public_def.level_defs import LogLevels
from tools.readers.reader_utils import (
    isFileInListValid,
)
from tools.loggers.simple_logger import loggerPrint

class ReaderBase:
    def __init__(self, fileList: list[str], fileExt: FileExt) -> None:
        if not isFileInListValid(fileList):
            loggerPrint("File in list not valid.", level=LogLevels.WARNING)
            exit(-1)
        self.fileList: list[str] = fileList
        self.fileExt: FileExt = fileExt

    def _load(self, fd: BufferedReader, registry: None) -> Any:
        pass

    def read(self):
        pass