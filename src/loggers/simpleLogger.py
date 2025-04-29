import sys
import os
import re
import inspect
from typing import Dict
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.publicDef.styleDefs import ANSIColors, ANSIStyles
from src.publicDef.levelDefs import LogLevels
from src.utils.timeTools import getCurrTimeInFmt, getCurrTime
from src.utils.configLoader import loadConfig

LOG_LEVEL_AND_COLOR_MATCH: Dict[LogLevels, ANSIColors] = {
    LogLevels.DEBUG:    ANSIColors.COLOR_BRIGHT_BLUE,
    LogLevels.INFO:     ANSIColors.COLOR_BRIGHT_GREEN,
    LogLevels.WARNING:  ANSIColors.COLOR_BRIGHT_YELLOW,
    LogLevels.ERROR:    ANSIColors.COLOR_BRIGHT_RED,
    LogLevels.CRITICAL: ANSIColors.COLOR_BRIGHT_MAGENTA,
}

MIN_LOG_LEVEL = loadConfig().get('min_log_level', LogLevels.INFO.value)

def loggerPrint(msg, level: LogLevels = LogLevels.INFO, frame = None) -> None:
    # 总是写入文件（直接写入，不经过stdout重定向）
    _writeToFile(msg, level, frame)

    # 控制台输出仅当级别足够时
    if level.value >= MIN_LOG_LEVEL:
        _printFormatted(msg, level, frame)

def _writeToFile(msg, level, frame):
    msg = re.sub(r'\033[[0-9]{1,}m', '', msg)
    logFile = f'logs/{getCurrTimeInFmt(fmt="%y-%m-%d")}.log'
    absPath = os.path.abspath(logFile)
    parentFolder = os.path.dirname(absPath)
    if not os.path.exists(parentFolder):
        os.makedirs(parentFolder)

    # 获取格式化日志内容（不含ANSI颜色代码）
    logContent = _formatForFile(msg, level, frame)

    with open(absPath, 'a') as f:
        f.write(logContent + '\n')

def _formatForFile(msg, level, frame):
    if not frame:
        frame = inspect.stack()[2]

    # 时间部分
    currTime = f"{getCurrTime():19}"

    # 文件路径部分
    filePath = os.path.relpath(frame.filename)
    lineNo = str(frame.lineno)
    fileContext = f'{filePath}:{lineNo}'
    fileContext = f'{fileContext:50}'

    # 日志级别
    levelStr = f"{level.name:8}"

    # 组合完整日志行
    return f"{currTime} {fileContext} {levelStr} {msg}"

def _printFormatted(msg, level, frame):
    colorStr: str = LOG_LEVEL_AND_COLOR_MATCH.get(level, ANSIColors.COLOR_RESET).value
    resetColorStr: str = ANSIColors.COLOR_RESET.value

    # 时间部分固定19字符宽度
    currTimeStr: str = ANSIColors.COLOR_BRIGHT_BLUE.value + f"{getCurrTime():19}" + resetColorStr + ' '

    # 文件路径部分完整显示，固定50字符宽度
    if not frame:
        frame = inspect.stack()[2]
    filePath = os.path.relpath(frame.filename)
    fileNameStr: str = f"{filePath}"

    # 日志级别固定8字符宽度
    levelStr: str = italicFont(boldFont(colorStr + f"{level.name:>8}" + ' '*4 + resetColorStr + ' '))

    lineNoStr: str = str(frame.lineno)
    fileContext: str = fileNameStr + ':' + lineNoStr + ' '
    fileContext: str = f'{fileContext:50}'

    print(currTimeStr + fileContext + levelStr + msg)

def loggerPrintList(dataList: list) -> None:
    if not isinstance(dataList, list):
        loggerPrint(f"Not a list.", frame=inspect.stack()[1], level=LogLevels.WARNING)
        return
    if dataList is not None and dataList != []:
        for item in dataList:
            if isinstance(item, dict):
                loggerPrintDict(item)
            else:
                # 向上回溯一层栈帧再打印
                loggerPrint(f"{item}", frame=inspect.stack()[1], level=LogLevels.DEBUG)

def loggerPrintDict(dataDict: dict) -> None:
    if not isinstance(dataDict, dict):
        loggerPrint(f"Not a dict.", frame=inspect.stack()[1], level=LogLevels.WARNING)
        return
    if dataDict is not None and dataDict != {}:
        for key, value in dataDict.items():
            loggerPrint(f"{key}: {value}", frame=inspect.stack()[1], level=LogLevels.DEBUG)

def _stylize(msg: str, style: ANSIStyles) -> str:
    return f"{style.value}{msg}{ANSIStyles.STYLE_RESET.value}"

def boldFont(msg: str) -> str:
    return _stylize(msg, ANSIStyles.STYLE_BOLD)

def italicFont(msg: str) -> str:
    return _stylize(msg, ANSIStyles.STYLE_ITALIC)

def loggerPrintBanner():
    loggerPrint(boldFont("""\033[31m██████╗░██████╗░░██████╗░░░░░░░███████╗██╗░░██╗████████╗██████╗░░█████╗░░█████╗░████████╗░█████╗░██████╗░\033[0m"""))
    loggerPrint(boldFont("""\033[35m██╔══██╗██╔══██╗██╔════╝░░░░░░░██╔════╝╚██╗██╔╝╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗\033[0m"""))
    loggerPrint(boldFont("""\033[34m██████╔╝██████╔╝██║░░██╗░█████╗█████╗░░░╚███╔╝░░░░██║░░░██████╔╝███████║██║░░╚═╝░░░██║░░░██║░░██║██████╔╝\033[0m"""))
    loggerPrint(boldFont("""\033[36m██╔══██╗██╔═══╝░██║░░╚██╗╚════╝██╔══╝░░░██╔██╗░░░░██║░░░██╔══██╗██╔══██║██║░░██╗░░░██║░░░██║░░██║██╔══██╗\033[0m"""))
    loggerPrint(boldFont("""\033[32m██║░░██║██║░░░░░╚██████╔╝░░░░░░███████╗██╔╝╚██╗░░░██║░░░██║░░██║██║░░██║╚█████╔╝░░░██║░░░╚█████╔╝██║░░██║\033[0m"""))
    loggerPrint(boldFont("""\033[33m╚═╝░░╚═╝╚═╝░░░░░░╚═════╝░░░░░░░╚══════╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝\033[0m"""))

if __name__ == '__main__':
    loggerPrint('haha', level=LogLevels.INFO)