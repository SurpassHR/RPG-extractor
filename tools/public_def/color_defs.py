from enum import StrEnum, IntEnum

class ANSIColors(StrEnum):
    COLOR_RESET             = "\033[0m"
    COLOR_BRIGHT_RED        = "\033[91m"
    COLOR_BRIGHT_GREEN      = "\033[92m"
    COLOR_BRIGHT_YELLOW     = "\033[93m"
    COLOR_BRIGHT_BLUE       = "\033[94m"
    COLOR_BRIGHT_MAGENTA    = "\033[95m"

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