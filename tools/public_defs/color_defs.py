from enum import StrEnum

class ANSIColors(StrEnum):
    COLOR_RESET             = "\033[0m"
    COLOR_BRIGHT_RED        = "\033[91m"
    COLOR_BRIGHT_GREEN      = "\033[92m"
    COLOR_BRIGHT_YELLOW     = "\033[93m"
    COLOR_BRIGHT_BLUE       = "\033[94m"
    COLOR_BRIGHT_MAGENTA    = "\033[95m"