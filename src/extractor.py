from src.loggers.simpleLogger import loggerPrint
from src.utils.autoRegister import ClassManager
from src.utils.fileTools import getAllFilesFromFolder, getFileExt, getFilesInFolderByType

from src.processers.readers import *
from src.processers.parsers import *
from src.processers.formatters import *
from src.processers.exporters import *

class Extractor:
    def __init__(self, dataFolder: str, outputFolder: str):
        self.classManager = ClassManager()
        self.dataFolder: str = dataFolder
        self.outputFolder: str = outputFolder
        self.fileList: list[str] = []
        self.targetFileExt: str = ''

        self.reader: ReaderBase = None
        self.parser: ParserBase = None
        self.formatter: FormatterBase = None
        self.exporter: ExporterBase = None

        self._init()

    # 推断目标文件拓展名
    def _inferFileExt(self) -> str:
        fileList = getAllFilesFromFolder(self.dataFolder)
        fileExtNum: dict[str, int] = {}
        if len(fileList) != 0:
            for file in fileList:
                fileExt = getFileExt(file).replace('.', '')
                fileExtNum[fileExt] = fileExtNum.get(fileExt, 0) + 1

        # 找到 data 目录下最多文件的拓展名
        maxNum = 0
        for file in fileExtNum:
            if fileExtNum[file] > maxNum:
                self.targetFileExt = file
                maxNum = fileExtNum[file]

        loggerPrint(f"{maxNum} files with ext '{self.targetFileExt}' is the most.")

    # 初始化各处理模块
    def _initProcessers(self):
        fileExt = self.targetFileExt.capitalize()

        self.fileList = getFilesInFolderByType(self.dataFolder, self.targetFileExt)
        self.reader = self.classManager.getReader(fileExt)(self.fileList)
        loggerPrint(f"Use Reader '{self.reader.__class__.__name__}'")

        self.parser = self.classManager.getParser(fileExt)()
        loggerPrint(f"Use Parser '{self.parser.__class__.__name__}'")

        self.formatter = self.classManager.getFormatter(fileExt)()
        loggerPrint(f"Use Formatter '{self.formatter.__class__.__name__}'")

        self.exporter = self.classManager.getExporter(fileExt)()
        loggerPrint(f"Use Exporter '{self.exporter.__class__.__name__}'")

    def _init(self):
        self._inferFileExt()
        self._initProcessers()

    def extract(self):
        pass
