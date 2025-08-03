from typing import Any
from src.utils.autoRegister import AutoRegisterBase
from src.utils.fileTools import FileTool


class InjecterBase(AutoRegisterBase, FileTool):
    def __init__(self, injectFolder: str, title: str = ""):
        self.injectFolder = injectFolder
        self.title = title

    def init(self):
        pass

    def inject(self, data: Any) -> None:
        pass
