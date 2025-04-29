import time
from functools import wraps
from src.loggers.simpleLogger import loggerPrint, LogLevels

def timer(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        startTime = time.time()
        res = func(*args, **kwargs)
        endTime = time.time()
        execTime = endTime - startTime

        className = ""
        if hasattr(args[0], '__class__'):
            className = f" (class: {args[0].__class__.__name__})"

        loggerPrint(f"Func '{func.__name__}'{className} exec time: {execTime:.4f} s.", level=LogLevels.INFO)
        return res
    return wrap