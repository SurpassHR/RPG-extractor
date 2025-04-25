
from typing import Any
from rubymarshal.classes import RubyObject
from src.processers.readers.readerBase import ReaderBase

class RxdataReader(ReaderBase):
    def __init__(self):
        super().__init__()  # 将str转换为list[str]以匹配父类签名

    def init(self, fileList: list[str]) -> list:
        pass