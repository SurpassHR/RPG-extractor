import os

from src.utils.fileTools import readJson

def loadConfig() -> dict:
    configFilePath = os.path.join('.', 'config.json')
    if not os.path.exists(configFilePath):
        raise FileNotFoundError(f"Config file not found: {configFilePath}")

    return readJson(configFilePath)