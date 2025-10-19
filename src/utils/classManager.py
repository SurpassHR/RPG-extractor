from typing import TYPE_CHECKING
from src.loggers.simpleLogger import boldFont, loggerPrint

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
    def register(cls, name: str, theClass):
        if "Base" in name:
            return

        if "Reader" in name:
            cls._readers[name.replace("Reader", "")] = theClass
            loggerPrint(f"Reg Reader {boldFont(f'{name}')}.")
        elif "Parser" in name:
            cls._parsers[name.replace("Parser", "")] = theClass
            loggerPrint(f"Reg Parser {boldFont(f'{name}')}.")
        elif "Formatter" in name:
            cls._formatters[name.replace("Formatter", "")] = theClass
            loggerPrint(f"Reg Formatter {boldFont(f'{name}')}.")
        elif "Exporter" in name:
            cls._exporters[name.replace("Exporter", "")] = theClass
            loggerPrint(f"Reg Exporter {boldFont(f'{name}')}.")
        elif "Injecter" in name:
            cls._injecters[name.replace("Injecter", "")] = theClass
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
