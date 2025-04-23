# Utilities for processing time

from datetime import datetime

def getCurrTime() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")