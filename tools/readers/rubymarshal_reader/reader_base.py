from typing import Any
from io import BufferedReader

class ReaderBase:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def _load(self, fd: BufferedReader, registry: None) -> Any:
        pass

    def read(self, filePath: str):
        pass