import logging

from typing import Any, Dict, Type

from snowflake.demos._demo_handle import DemoHandle


logger = logging.getLogger(__name__)


class SingletonMeta(type):
    _instances: Dict[Type[Any], Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class DemosLoader(metaclass=SingletonMeta):
    _loaded_demos: Dict[str, DemoHandle] = {}

    def __init__(self):
        pass

    def get_demo_handle(self, name: str, refresh_demo: bool = False) -> DemoHandle:
        if name not in self._loaded_demos or refresh_demo:
            logger.debug("Loading demo %s", name)
            self._loaded_demos[name] = DemoHandle(name)
            self._loaded_demos[name]._setup_handle(refresh_demo)
        elif not self._loaded_demos[name]._setup_complete:
            self._loaded_demos[name]._setup_handle(True)
        return self._loaded_demos[name]
