# rgssReader 是 rubymarshallReader 的升级版

from typing import override

from src.publicDef.levelDefs import LogLevels
from src.loggers.simpleLogger import boldFont, loggerPrint
from src.processers.readers.readerBase import ReaderBase
from src.utils.decorators.execTimer import timer
from src.utils.rgssToolCaller import RgssToolCaller


class RgssReader(ReaderBase):
    def __init__(self):
        super().__init__()
        self.rgssToolCaller = RgssToolCaller()

    @timer
    @override
    def read(self) -> tuple[list, dict, list]:
        super().read()

        if not self.fileList:
            loggerPrint(f"File list is empty.", level=LogLevels.WARNING)
            exit(-1)

        # 应当为一个数据文件的列表
        rgssData = []
        # 将父类的 fileList 通过 ',' 分隔，合并为一个字符串
        fileListStr: str = ",".join(self.fileList)
        print(fileListStr)

        return [], {}, []


if __name__ == "__main__":
    reader = RgssReader()
    reader.read()
