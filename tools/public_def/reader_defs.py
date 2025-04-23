import re
from enum import Enum, StrEnum, IntEnum

class FileExt(StrEnum):
    RXDATA = '.rxdata'
    RVDATA = '.rvdata'
    JSON   = '.json'

class ReFileType(Enum):
    SCRIPTS = re.compile('Scripts.rxdata')
    DOODAS  = re.compile(r'\w*_doodads.rxdata')
    COMMON  = re.compile(r'.*.rxdata')
    ALL     = re.compile(r'.*')

class RubyObjAttrCode(IntEnum):
    TITLE = 101 # 标题
    OPTION = 102 # 选项
    TEXT_DISP = 401 # 文本显示