import os
import json
from typing import Any, Optional
from pathlib import Path

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


def setConfig(key: str, value: Any) -> bool:
    try:
        config_path = os.path.join("config.json")
        Path(os.path.dirname(config_path)).mkdir(parents=True, exist_ok=True)

        config = loadConfig()
        keys = key.split(".")
        current = config
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value

        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        return True
    except Exception:
        return False


def getConfig(key: str, default: Optional[Any] = None) -> Any:
    try:
        config = loadConfig()
        keys = key.split(".")
        current = config
        for k in keys:
            if k not in current:
                return default
            current = current[k]
        return current
    except Exception:
        return default
