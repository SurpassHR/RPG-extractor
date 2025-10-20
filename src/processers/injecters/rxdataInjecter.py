from src.processers.injecters.injecterBase import InjecterBase


class RxdataInjecter(InjecterBase):
    """
    desc: Ruby Marshal 文件注入器
    """

    def __init__(self):
        super().__init__()

    def init(self, gameDataFolder: str, backupFolder: str = ""):
        return super().init(gameDataFolder, backupFolder)

    def inject(self, data: str | dict[str, str]) -> None:
        return super().inject(data)
