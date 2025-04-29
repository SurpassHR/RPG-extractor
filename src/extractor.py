from src.publicDef.levelDefs import LogLevels
from src.loggers.simpleLogger import loggerPrint, boldFont
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

        self.reader: ReaderBase
        self.parser: ParserBase
        self.formatter: FormatterBase
        self.exporter: ExporterBase

        self._init()

    # 推断目标文件拓展名
    def _inferFileExt(self):
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

        loggerPrint(f"{maxNum} files with ext '{boldFont(self.targetFileExt)}' is the most.")

    # 初始化各处理模块
    def _initProcessers(self):
        fileExt = self.targetFileExt.capitalize()

        self.fileList = getFilesInFolderByType(self.dataFolder, self.targetFileExt)
        readerCls = self.classManager.getReader(fileExt)
        if readerCls:
            self.reader = readerCls()
            loggerPrint(f"Use Reader {boldFont(f'{self.reader.__class__.__name__}')}")
        else:
            loggerPrint(f"Procsr '{boldFont(f"{self.targetFileExt}Reader")}' not found.", level=LogLevels.CRITICAL)
            exit(-1)

        parserCls = self.classManager.getParser(fileExt)
        if parserCls:
            self.parser = parserCls()
            loggerPrint(f"Use Parser {boldFont(f'{self.parser.__class__.__name__}')}")
        else:
            loggerPrint(f"Procsr '{boldFont(f"{self.targetFileExt}Parser")}' not found.", level=LogLevels.CRITICAL)
            exit(-1)

        formatterCls = self.classManager.getFormatter(fileExt)
        if formatterCls:
            self.formatter = formatterCls()
            loggerPrint(f"Use Formatter {boldFont(f'{self.formatter.__class__.__name__}')}")
        else:
            loggerPrint(f"Procsr '{boldFont(f"{self.targetFileExt}Formatter")}' not found.", level=LogLevels.CRITICAL)
            exit(-1)

        exporterCls = self.classManager.getExporter(fileExt)
        if exporterCls:
            self.exporter = exporterCls(self.outputFolder)
            loggerPrint(f"Use Exporter {boldFont(f'{self.exporter.__class__.__name__}')}")
        else:
            loggerPrint(f"Procsr '{boldFont(f"{self.targetFileExt}Exporter")}' not found.", level=LogLevels.CRITICAL)
            exit(-1)

    def _init(self):
        self._inferFileExt()
        self._initProcessers()

        self.reader.init(self.fileList)
        self.parser.init()
        self.formatter.init()
        self.exporter.init()

    def extract(self):
        readData = self.reader.read()
        parseData = self.parser.parse(readData)
        formatData = self.formatter.format(parseData)
        self.exporter.export(formatData)