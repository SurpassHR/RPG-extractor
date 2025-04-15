from enum import StrEnum, IntEnum

class FileType(StrEnum):
    RXDATA = '.rxdata'
    RVDATA = '.rvdata'

class RubyObjAttrCode(IntEnum):
    TITLE = 101 # 标题
    OPTION = 102 # 选项
    TEXT_DISP = 401 # 文本显示

class ColorCode(IntEnum):
    # 参考: https://essentialsdocs.fandom.com/wiki/Messages#Text_colours
    BLUE = 1
    RED = 2
    GREEN = 3
    CYAN = 4
    MAGENTA = 5
    YELLOW = 6
    GRAY = 7
    WHITE = 8
    PURPLE = 9
    ORANGE = 10
    DARK_DEFAULT = 11
    LIGHT_DEFAULT = 12