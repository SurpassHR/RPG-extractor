from src.loggers.simpleLogger import boldFont, loggerPrint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.processers.readers.readerBase import ReaderBase
    from src.processers.parsers.parserBase import ParserBase
    from src.processers.exporters.exporterBase import ExporterBase
    from src.processers.formatters.formatterBase import FormatterBase
    from src.processers.injecters.injecterBase import InjecterBase


# 定义一个注册中心（管理类）
class ClassManager:
    _readers: dict[str, "ReaderBase"] = {}
    _parsers: dict[str, "ParserBase"] = {}
    _exporters: dict[str, "ExporterBase"] = {}
    _formatters: dict[str, "FormatterBase"] = {}
    _injecters: dict[str, "InjecterBase"] = {}

    @classmethod
    def register(cls, name: str, the_class):
        if "Base" in name:
            return

        if "Reader" in name:
            cls._readers[name.replace("Reader", "")] = the_class
            loggerPrint(f"Reg Reader {boldFont(f'{name}')}.")
        elif "Parser" in name:
            cls._parsers[name.replace("Parser", "")] = the_class
            loggerPrint(f"Reg Parser {boldFont(f'{name}')}.")
        elif "Formatter" in name:
            cls._formatters[name.replace("Formatter", "")] = the_class
            loggerPrint(f"Reg Formatter {boldFont(f'{name}')}.")
        elif "Exporter" in name:
            cls._exporters[name.replace("Exporter", "")] = the_class
            loggerPrint(f"Reg Exporter {boldFont(f'{name}')}.")
        elif "Injecter" in name:
            cls._injecters[name.replace("Injecter", "")] = the_class
            loggerPrint(f"Reg Injecter {boldFont(f'{name}')}.")

    @classmethod
    def getReader(cls, name):
        return cls._readers.get(name)

    @classmethod
    def getParser(cls, name):
        return cls._parsers.get(name)

    @classmethod
    def getFormatter(cls, name):
        return cls._formatters.get(name)

    @classmethod
    def getExporter(cls, name):
        return cls._exporters.get(name)

    @classmethod
    def getInjecter(cls, name):
        return cls._injecters.get(name)

    @classmethod
    def listReaders(cls):
        loggerPrint(f"{cls._readers}")

    @classmethod
    def listParsers(cls):
        loggerPrint(f"{cls._parsers}")

    @classmethod
    def listFormatters(cls):
        loggerPrint(f"{cls._formatters}")

    @classmethod
    def listExporters(cls):
        loggerPrint(f"{cls._exporters}")

    @classmethod
    def listInjecters(cls):
        loggerPrint(f"{cls._injecters}")


# 定义一个元类
class AutoRegisterMeta(type):
    # __new__ 是创建类对象时调用的方法
    def __new__(cls, name, bases, dct):
        # 先调用父类（type）的 __new__ 方法创建类对象
        newClass = super().__new__(cls, name, bases, dct)

        # 在类创建后，将类注册到 ClassRegistry 中
        # 避免注册元类本身或者基类（如果不想注册基类的话）
        if name != "AutoRegisterBase" and name != "AutoRegisterMeta":
            # 可以选择使用类的 __name__ 或者 dct['__name__'] 作为注册名
            ClassManager.register(name, newClass)

        # 返回新创建的类对象
        return newClass


class AutoRegisterBase(metaclass=AutoRegisterMeta):
    pass
