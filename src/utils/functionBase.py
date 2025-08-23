from enum import IntEnum
from typing import Any


class EventEmitter:
    class EventEnum(IntEnum):
        GET_RAW_DATA = 0
        GET_PARSED_DATA = 1
        GET_FORMATTED_DATA = 2

    _singleton = None

    def __init__(self):
        self._handlers = {}

    @staticmethod
    def getSingleton():
        if EventEmitter._singleton is None:
            EventEmitter._singleton = EventEmitter()
        return EventEmitter._singleton

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.getSingleton()

    def subscribe(self, eventName, handler):
        if eventName not in self._handlers:
            self._handlers[eventName] = []
        self._handlers[eventName].append(handler)

    def emit(self, eventName, data):
        if eventName in self._handlers:
            for handler in self._handlers[eventName]:
                handler(data)


eventEmitter = EventEmitter()
