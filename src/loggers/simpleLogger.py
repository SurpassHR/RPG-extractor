import sys
import os
import inspect
from typing import Dict
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.publicDef.colorDefs import ANSIColors
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
    log_file = f'logs/{getCurrTimeInFmt(fmt="%y-%m-%d")}.log'
    abs_path = os.path.abspath(log_file)
    parent_folder = os.path.dirname(abs_path)
    if not os.path.exists(parent_folder):
        os.makedirs(parent_folder)

    # 获取格式化日志内容（不含ANSI颜色代码）
    log_content = _formatForFile(msg, level, frame)

    with open(abs_path, 'a') as f:
        f.write(log_content + '\n')

def _formatForFile(msg, level, frame):
    if not frame:
        frame = inspect.stack()[2]

    # 时间部分
    curr_time = f"{getCurrTime():19}"

    # 文件路径部分
    file_path = os.path.relpath(frame.filename)
    line_no = str(frame.lineno)
    file_context = f'{file_path}:{line_no}'
    file_context = f'{file_context:50}'

    # 日志级别
    level_str = f"{level.name:8}"

    # 组合完整日志行
    return f"{curr_time} {file_context} {level_str} {msg}"

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
    levelStr: str = colorStr + f"{level.name:8}" + resetColorStr + ' '

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

def loggerPrintBanner():
    loggerPrint(r""",-.  ;-.   ,-.     ,--. .   , ,---. ,-.   ,.   ,-. ,---.  ,-.  ,-.  """)
    loggerPrint(r"""|  ) |  ) /        |     \ /    |   |  ) /  \ /      |   /   \ |  ) """)
    loggerPrint(r"""|-<  |-'  | -. --- |-     X     |   |-<  |--| |      |   |   | |-<  """)
    loggerPrint(r"""|  \ |    \  |     |     / \    |   |  \ |  | \      |   \   / |  \ """)
    loggerPrint(r"""'  ' '     `-'     `--' '   `   '   '  ' '  '  `-'   '    `-'  '  ' """)

if __name__ == '__main__':
    loggerPrint('haha', level=LogLevels.INFO)
