import os
import sys
import shlex
from pathlib import Path
from enum import StrEnum
from typing import overload

sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent.parent))

from src.loggers.simpleLogger import loggerPrint, loggerPrintList
from src.publicDef.levelDefs import LogLevels


class RgssToolCaller:
    """
    desc: 调用 rgss 工具
    """

    class FuncName(StrEnum):
        VERBOSE = "--verbose"
        INPUT_FILE = "--input-file"
        OUTPUT_FILE = "--output-file"
        INPUT_FILE_LIST = "--input-file-list"
        OUTPUT_FILE_LIST = "--output-file-list"
        SOURCE_DIR = "--source-dir"
        DEST_DIR = "--dest-dir"
        TARGET_EXT = "--target-ext"
        HELP = "--help"

    def __init__(self) -> None:
        self._detectSubmodule()

    def _detectSubmodule(self):
        absPath = os.path.abspath("./")
        lsDir = os.listdir(absPath)
        if ".projRootMark" in lsDir:
            if "rgsspacker" not in lsDir:
                loggerPrint("rgsspacker submodule not found.", LogLevels.ERROR)
                exit(1)
            else:
                loggerPrint("rgsspacker submodule found.", LogLevels.INFO)
                self.rgss_extractor = os.path.join(absPath, "rgsspacker", "rgss_extractor.rb")
        else:
            loggerPrint(".projRootMark not found.", LogLevels.ERROR)
            exit(1)

        # 测试调用
        self._funcCallNoRet([self.FuncName.HELP])

    def convSingleFile(self, inFilePath: str, outFilePath: str):
        self._funcCallNoRet(
            [
                self.FuncName.INPUT_FILE,
                inFilePath,
                self.FuncName.OUTPUT_FILE,
                outFilePath,
            ]
        )

    @overload
    def convMultiFiles(self, inFileList: list[str], outFileList: list[str]) -> None:
        ...

    # 声明第二个重载签名：处理文件夹路径
    @overload
    def convMultiFiles(self, srcFolder: str, dstFolder: str) -> None:
        ...

    # 提供统一的实现
    def convMultiFiles(self, *args, **kwargs) -> None:
        # 优先检查关键字参数，因为它们更明确
        if 'inFileList' in kwargs and 'outFileList' in kwargs:
            inFileList = kwargs['inFileList']
            outFileList = kwargs['outFileList']
            # 为了代码健壮性，仍然可以进行类型检查
            if isinstance(inFileList, list) and isinstance(outFileList, list):
                self._funcCallNoRet(
                    [
                        self.FuncName.INPUT_FILE_LIST,
                        ",".join(inFileList),
                        self.FuncName.OUTPUT_FILE_LIST,
                        ",".join(outFileList),
                    ]
                )
                return

        if 'srcFolder' in kwargs and 'dstFolder' in kwargs:
            srcFolder = kwargs['srcFolder']
            dstFolder = kwargs['dstFolder']
            if isinstance(srcFolder, str) and isinstance(dstFolder, str):
                self._funcCallNoRet(
                    [
                        self.FuncName.SOURCE_DIR,
                        srcFolder,
                        self.FuncName.DEST_DIR,
                        dstFolder,
                    ]
                )
                return

        # 如果没有关键字参数，则检查位置参数
        if len(args) == 2:
            arg1, arg2 = args
            if isinstance(arg1, list) and isinstance(arg2, list):
                # 对应 (inFileList, outFileList)
                self._funcCallNoRet(
                    [
                        self.FuncName.INPUT_FILE_LIST,
                        ",".join(arg1),
                        self.FuncName.OUTPUT_FILE_LIST,
                        ",".join(arg2),
                    ]
                )
                return
            elif isinstance(arg1, str) and isinstance(arg2, str):
                # 对应 (srcFolder, dstFolder)
                self._funcCallNoRet(
                    [
                        self.FuncName.SOURCE_DIR,
                        arg1,
                        self.FuncName.DEST_DIR,
                        arg2,
                    ]
                )
                return

        # 如果所有情况都不匹配，抛出异常
        raise TypeError("Invalid arguments for convMultiFiles")

    def _funcCall(self, argList: list[str]):
        quoted_args = [shlex.quote(arg) for arg in argList]
        return os.popen(f"ruby {self.rgss_extractor} {' '.join(quoted_args)}").read()

    def _funcCallNoRet(self, argList: list[str]):
        loggerPrintList(self._funcCall(argList).split("\n"), level=LogLevels.INFO)


if __name__ == "__main__":
    rvPackerCaller = RgssToolCaller()
    rvPackerCaller.convSingleFile(
        r"E:\Games\25-03-31\Curse of Pleasure v0.9\Data\Map005.rxdata".replace("\\", "/"),
        "./Map005.yaml",
    )
