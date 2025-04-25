from src.loggers.simpleLogger import loggerPrint

# 定义一个注册中心（管理类）
class ClassManager:
    _readers = {}
    _parsers = {}
    _exporters = {}
    _formatters = {}

    @classmethod
    def register(cls, name: str, the_class):
        if 'Base' in name:
            return

        if 'Reader' in name:
            cls._readers[name.replace('Reader', '')] = the_class
            loggerPrint(f"Reader '{name}' registered.")
        elif 'Parser' in name:
            cls._parsers[name.replace('Parser', '')] = the_class
            loggerPrint(f"Parser '{name}' registered.")
        elif 'Formatter' in name:
            cls._formatters[name.replace('Formatter', '')] = the_class
            loggerPrint(f"Formatter '{name}' registered.")
        elif 'Exporter' in name:
            cls._exporters[name.replace('Exporter', '')] = the_class
            loggerPrint(f"Exporter '{name}' registered.")

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

# 定义一个元类
class AutoRegisterMeta(type):
    # __new__ 是创建类对象时调用的方法
    def __new__(cls, name, bases, dct):
        # 先调用父类（type）的 __new__ 方法创建类对象
        newClass = super().__new__(cls, name, bases, dct)

        # 在类创建后，将类注册到 ClassRegistry 中
        # 避免注册元类本身或者基类（如果不想注册基类的话）
        if name != 'AutoRegisterBase' and name != 'AutoRegisterMeta':
            # 可以选择使用类的 __name__ 或者 dct['__name__'] 作为注册名
            ClassManager.register(name, newClass)

        # 返回新创建的类对象
        return newClass

class AutoRegisterBase(metaclass=AutoRegisterMeta):
    pass