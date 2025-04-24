import sys
import os
import inspect
from typing import Dict
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.publicDef.colorDefs import ANSIColors
from src.publicDef.levelDefs import LogLevels
from src.utils.timeTools import getCurrTime

LOG_LEVEL_AND_COLOR_MATCH: Dict[LogLevels, ANSIColors] = {
    LogLevels.DEBUG:    ANSIColors.COLOR_BRIGHT_BLUE,
    LogLevels.INFO:     ANSIColors.COLOR_BRIGHT_GREEN,
    LogLevels.WARNING:  ANSIColors.COLOR_BRIGHT_YELLOW,
    LogLevels.ERROR:    ANSIColors.COLOR_BRIGHT_RED,
    LogLevels.CRITICAL: ANSIColors.COLOR_BRIGHT_MAGENTA,
}

def loggerPrint(msg, level: LogLevels = LogLevels.INFO, frame = None) -> None:
    colorStr: str = LOG_LEVEL_AND_COLOR_MATCH.get(level, ANSIColors.COLOR_RESET).value
    resetColorStr: str = ANSIColors.COLOR_RESET.value

    # 时间部分固定19字符宽度
    currTimeStr: str = ANSIColors.COLOR_BRIGHT_BLUE.value + f"{getCurrTime():19}" + resetColorStr + ' '

    # 文件路径部分完整显示，固定50字符宽度
    if not frame:
        frame = inspect.stack()[1]
    filePath = os.path.relpath(frame.filename)
    fileNameStr: str = f"{filePath}"

    # 日志级别固定8字符宽度
    levelStr: str = colorStr + f"{level.value:8}" + resetColorStr + ' '

    lineNoStr: str = str(frame.lineno)
    fileContext: str = fileNameStr + ':' + lineNoStr + ' '
    fileContext: str = f'{fileContext:50}'

    print(currTimeStr + fileContext + levelStr + msg)

def printList(dataList: list) -> None:
    if dataList is not None and dataList != []:
        for item in dataList:
            # 向上回溯一层栈帧再打印
            loggerPrint(item, frame=inspect.stack()[1])

if __name__ == '__main__':
    loggerPrint('haha', level=LogLevels.DEBUG)
