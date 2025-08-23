from src.processers.injecters.injecterBase import InjecterBase


class RxdataInjecter(InjecterBase):
    def init(self, gameDataFolder: str, backupFolder: str = ""):
        return super().init(gameDataFolder, backupFolder)
