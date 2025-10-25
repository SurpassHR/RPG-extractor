import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.processers.readers import ReaderBase
from src.processers.readers.rgssReader import RgssReader


def testRead():
    reader: ReaderBase = RgssReader()
    fileList = [
        "E:/Games/25-10-18/The_Curse_of_Pleasure_v1.0/The Curse of Pleasure v1.0/Data/Map001.rxdata",
        "E:/Games/25-10-18/The_Curse_of_Pleasure_v1.0/The Curse of Pleasure v1.0/Data/Map002.rxdata",
    ]
    reader.init(fileList=fileList)
    # assert reader.read() == []
    reader.read()


if __name__ == "__main__":
    testRead()
