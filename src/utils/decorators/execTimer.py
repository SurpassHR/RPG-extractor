import time
from functools import wraps
from src.loggers.simpleLogger import boldFont, loggerPrint, LogLevels


def timer(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        startTime = time.time()
        res = func(*args, **kwargs)
        endTime = time.time()
        execTime = endTime - startTime

        className = ""
        if hasattr(args[0], "__class__"):
            className = args[0].__class__.__name__
        fullFuncName = boldFont(f"{className}::{func.__name__}")

        loggerPrint(f"Func '{fullFuncName}' exec time: {execTime:.4f} s.", level=LogLevels.INFO)
        return res

    return wrap
