from src.utils.classManager import ClassManager


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
