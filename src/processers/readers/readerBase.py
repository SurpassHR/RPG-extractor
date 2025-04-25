from typing import Any
from src.utils.autoRegister import AutoRegisterBase

class ReaderBase(AutoRegisterBase):
    def __init__(self, fileList: list[str]):
        self.fileList = fileList

    def read(self):
        pass

    def get(self) -> Any:
        pass