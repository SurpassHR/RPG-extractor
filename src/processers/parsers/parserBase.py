from typing import Any

from src.utils.autoRegister import AutoRegisterBase

class ParserBase(AutoRegisterBase):
    def __init__(self):
        pass

    def init(self):
        pass

    def parse(self, data: Any) -> Any:
        pass