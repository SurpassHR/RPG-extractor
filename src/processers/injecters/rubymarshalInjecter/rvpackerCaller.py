import os
import sys
from pathlib import Path
from enum import StrEnum
import shlex

sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent.parent))

from src.loggers.simpleLogger import loggerPrint, loggerPrintList
from src.publicDef.levelDefs import LogLevels


class RvpackerCaller:
    """
    desc: 调用rvpacker
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
        pass

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
        self.funcCallNoRet([self.FuncName.HELP])

    def extractSingleFile(self, inFilePath: str, outFilePath: str):
        self.funcCallNoRet(
            [
                self.FuncName.INPUT_FILE,
                inFilePath,
                self.FuncName.OUTPUT_FILE,
                outFilePath,
            ]
        )

    def funcCall(self, argList: list[str]):
        quoted_args = [shlex.quote(arg) for arg in argList]
        return os.popen(f"ruby {self.rgss_extractor} {' '.join(quoted_args)}").read()

    def funcCallNoRet(self, argList: list[str]):
        loggerPrintList(self.funcCall(argList).split("\n"), level=LogLevels.INFO)


if __name__ == "__main__":
    rvPackerCaller = RvpackerCaller()
    rvPackerCaller._detectSubmodule()
    rvPackerCaller.extractSingleFile(
        r"E:\Games\25-03-31\Curse of Pleasure v0.9\Data\Map005.rxdata".replace("\\", "/"),
        "./Map005.yaml",
    )
