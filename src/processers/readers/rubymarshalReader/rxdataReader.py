
import sys
from pathlib import Path
from io import BufferedReader
from typing import Any
from rubymarshal.classes import RubyObject
from src.processers.readers.readerBase import ReaderBase

class RxdataReader(ReaderBase):
    def __init__(self, fileList: list[str]):
        super().__init__(fileList)  # 将str转换为list[str]以匹配父类签名