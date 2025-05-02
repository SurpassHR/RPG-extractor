from datetime import datetime

def getCurrTimeInFmt(fmt: str) -> str:
    return datetime.now().strftime(fmt)

def getCurrTime() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")