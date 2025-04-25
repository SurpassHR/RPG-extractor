from typing import Any
from src.utils.autoRegister import AutoRegisterBase

class ReaderBase(AutoRegisterBase):
    def __init__(self):
        pass

    def init(self, fileList: list[str]) -> None:
        self.fileList = fileList

    def read(self) -> Any:
        pass