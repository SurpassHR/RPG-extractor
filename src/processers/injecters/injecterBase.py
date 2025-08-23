from os import path
from typing import Union

from src.loggers.simpleLogger import loggerPrint
from src.utils.autoRegister import AutoRegisterBase
from src.utils.fileTools import FileTool, copyFolder, readJson
from src.utils.decorators.execTimer import timer


class TrDict:
    """
    desc: 翻译字典
    """

    def __init__(self, trDict: Union[str, dict]) -> None:
        self.trDict: dict[str, str] = readJson(trDict) if isinstance(trDict, str) else trDict

    def getTr(self, key: str) -> str:
        """
        desc: 获取翻译结果
        params:
            key: 翻译键，若键不存在则返回原字符串
        """
        if key not in self.trDict:
            # loggerPrint(f"Translation key '{key}' not found.")
            return key
        return self.trDict[key]


class InjecterBase(AutoRegisterBase, FileTool):
    """
    desc: 注入器基类
    """

    def __init__(self):
        pass

    def init(self, gameDataFolder: str, backupFolder: str = ""):
        self.gameDataFolder = gameDataFolder
        self.backupFolder = (
            path.abspath(path.join(gameDataFolder, "../dataBackup")) if backupFolder == "" else backupFolder
        )

    @timer
    def inject(self, data: Union[str, dict[str, str]]) -> None:
        """
        params:
            data: 可以是翻译文件路径，也可以是翻译字典
        """
        # 将原始数据备份到备份文件夹
        self._backupFolder()
        # 加载翻译字典
        self.trDict: TrDict = TrDict(data)

    def _backupFolder(self):
        try:
            copyFolder(self.gameDataFolder, self.backupFolder)
        except Exception as e:
            loggerPrint(f"Backup data failed: {e}")
        loggerPrint(f"Backup data to {self.backupFolder}")
