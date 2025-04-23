import sys
import os
import inspect
from typing import Dict
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from tools.public_defs.color_defs import ANSIColors
from tools.public_defs.level_defs import LogLevels
from tools.time_utils import getCurrTime

LOG_LEVEL_AND_COLOR_MATCH: Dict[LogLevels, ANSIColors] = {
    LogLevels.DEBUG: ANSIColors.COLOR_BRIGHT_BLUE,
    LogLevels.INFO: ANSIColors.COLOR_BRIGHT_GREEN,
    LogLevels.WARNING: ANSIColors.COLOR_BRIGHT_YELLOW,
    LogLevels.ERROR: ANSIColors.COLOR_BRIGHT_RED,
    LogLevels.CRITICAL: ANSIColors.COLOR_BRIGHT_MAGENTA,
}

def _getLineNumber() -> str:
    return str(inspect.currentframe().f_back.f_lineno) # type: ignore

def loggerPrint(
    msg,
    logLevel: LogLevels = LogLevels.INFO
) -> None:
    colorStr: str = LOG_LEVEL_AND_COLOR_MATCH.get(logLevel, ANSIColors.COLOR_RESET).value
    resetColorStr: str = ANSIColors.COLOR_RESET.value

    levelStr: str = colorStr + logLevel.value + resetColorStr + '\t'
    currTimeStr: str = ANSIColors.COLOR_BRIGHT_BLUE.value + getCurrTime() + ANSIColors.COLOR_RESET.value + '\t'

    fileNameStr: str = os.path.realpath(os.path.basename(__file__))
    lineNoStr: str = _getLineNumber()
    fileContext: str = fileNameStr + ':' + lineNoStr + '\t'
    print(currTimeStr + fileContext + levelStr + msg, sep='')

if __name__ == '__main__':
    loggerPrint('haha', logLevel=LogLevels.DEBUG)
