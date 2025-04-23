import sys
import json
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from tools.readers.reader_utils import (
    isFileExists,
)

def loadJson(filePath: str) -> dict:
    if not isFileExists(filePath):
        return {}

    with open(filePath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data