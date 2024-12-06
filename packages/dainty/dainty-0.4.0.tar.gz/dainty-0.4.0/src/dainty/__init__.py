import importlib.metadata

from .dainty import DaintyExtras, DaintyModel

__version__ = importlib.metadata.version("dainty")

__all__ = [
    "DaintyExtras",
    "DaintyModel",
]
