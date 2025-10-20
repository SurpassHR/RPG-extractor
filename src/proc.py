from enum import IntEnum

from src.publicDef.levelDefs import LogLevels
from src.loggers.simpleLogger import loggerPrint, boldFont

from src.utils.autoRegister import ClassManager
from src.utils.fileTools import getAllFilesFromFolder, getFileExt, getFilesInFolderByType, readJson
from src.utils.decorators.execTimer import timer

from src.processers.readers import ReaderBase
from src.processers.parsers import ParserBase
from src.processers.formatters import FormatterBase
from src.processers.exporters import ExporterBase
from src.processers.injecters import InjecterBase


class Proc:
    class ProcMode(IntEnum):
        Extract = 0
        Inject = 1

    class PrcsrType(IntEnum):
        Reader = 0
        Parser = 1
        Formatter = 2
        Exporter = 3
        Injecter = 4

    def __init__(
        self,
        dataFolder: str,
        outputFolder: str,
        trFolder: str = "",
        title: str = "",
        format: bool = False,
        mode: ProcMode = ProcMode.Extract,
    ):
        """
        desc: 初始化
        params:
            dataFolder: 游戏数据文件夹路径
            outputFolder: 输出文件夹路径，当模式为 Inject 时，用于写入数据文件
            title: 标题
            format: 是否格式化
            mode: 处理模式
        """
        # 自动注册
        self.classManager: ClassManager = ClassManager()

        # 用户配置
        self.dataFolder: str = dataFolder
        self.outputFolder: str = outputFolder
        self.trFolder: str = trFolder

        # 临时变量
        self.title: str = title
        self.fileList: list[str] = []
        self.targetFileExt: str = ""
        self.execFormat: bool = format

        # 处理模式
        self.mode: Proc.ProcMode = mode

        # 处理模块
        self.reader: ReaderBase
        self.parser: ParserBase
        self.formatter: FormatterBase
        self.exporter: ExporterBase
        self.injecter: InjecterBase

        self._init()

    def changeMode(self):
        """
        desc: 切换处理模式
        """
        if self.mode == self.ProcMode.Extract:
            self.mode = self.ProcMode.Inject
        else:
            self.mode = self.ProcMode.Extract

    def getMode(self):
        """
        desc: 获取当前处理模式
        """
        return self.mode

    # 推断目标文件拓展名
    def _inferFileExt(self):
        """
        desc: 推断目标文件拓展名
        """
        fileList = getAllFilesFromFolder(self.dataFolder)
        if fileList == []:
            loggerPrint(msg=f"Data folder [{self.dataFolder}] contains no file!", level=LogLevels.CRITICAL)
            exit(-1)

        fileExtNum: dict[str, int] = {}
        if len(fileList) != 0:
            for file in fileList:
                fileExt = getFileExt(file).replace(".", "")
                fileExtNum[fileExt] = fileExtNum.get(fileExt, 0) + 1

        # 找到 data 目录下最多文件的拓展名
        maxNum = 0
        for file in fileExtNum:
            if fileExtNum[file] > maxNum:
                self.targetFileExt = file
                maxNum = fileExtNum[file]

        loggerPrint(f"Infering target file ext to be '{boldFont(self.targetFileExt)}', count: {maxNum}.")

    # 初始化各处理模块
    def _initPrcsr(self, prcsrType: PrcsrType, *initArgs) -> None:
        """
        通过从类管理器获取其类，将其赋值给一个实例属性，并调用其初始化方法，来初始化一个处理器（如读取器、解析器等）。
        """
        fileExt = self.targetFileExt.capitalize()
        # 例如，prcsrType = "Reader" -> getter_name = "getReader"
        getter = getattr(self.classManager, f"get{prcsrType.name}")
        processorCls = getter(fileExt)

        if processorCls:
            # 例如，prcsrType = "Reader" 变为 attr_name = "reader"
            attrName = prcsrType.name.lower()

            setattr(self, attrName, processorCls())

            processorInstance = getattr(self, attrName)
            processorInstance.init(*initArgs)

            loggerPrint(f"Use {prcsrType.name} {boldFont(f'{processorInstance.__class__.__name__}')}.")
        else:
            loggerPrint(
                f"Procsr '{boldFont(f'{self.targetFileExt}{prcsrType.name}')}' not found.",
                level=LogLevels.CRITICAL,
            )
            exit(-1)

    def _initProcessers(self):
        """
        desc: 初始化各处理模块
        """
        self.fileList = getFilesInFolderByType(self.dataFolder, self.targetFileExt)

        self._initPrcsr(self.PrcsrType.Reader, self.fileList)
        self._initPrcsr(self.PrcsrType.Parser)
        self._initPrcsr(self.PrcsrType.Formatter)

        if self.mode == self.ProcMode.Extract:
            self._initPrcsr(self.PrcsrType.Exporter, self.outputFolder, self.title)
        else:
            self._initPrcsr(self.PrcsrType.Injecter, self.outputFolder, self.title)

    def _init(self):
        self._inferFileExt()
        self._initProcessers()

    @timer
    def extract(self):
        readData = self.reader.read()
        parseData = self.parser.parse(readData)
        extractData = self.formatter.format(parseData) if self.execFormat else parseData
        self.exporter.export(extractData)

    @timer
    def inject(self, jsonPath: str):
        translateData: dict[str, str] = readJson(jsonPath)
        self.injecter.inject(translateData)

    def proc(self):
        if self.getMode() == self.ProcMode.Extract:
            self.extract()
        else:
            self.inject(self.trFolder)
