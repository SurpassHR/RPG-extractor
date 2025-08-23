import os

from src.utils.fileTools import readJson


def getProjectRoot():
    current_dir = os.path.abspath(__file__)
    while True:
        if os.path.exists(os.path.join(current_dir, ".projRootMark")):  # 替换为你的标识文件
            return current_dir
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:  # 防止到达文件系统根目录
            raise FileNotFoundError("找不到项目根目录的标识文件")
        current_dir = parent_dir


def loadConfig() -> dict:
    configFilePath = os.path.join(getProjectRoot(), "config.json")
    if not os.path.exists(configFilePath):
        raise FileNotFoundError(f"Config file not found: {configFilePath}")

    return readJson(configFilePath)
