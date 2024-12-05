# ~/DeclarativeEnum/src/declarativeenum/__init__.py
from .core import DeclarativeEnum
from .exceptions import DeclarativeEnumError, PreprocessError, ValidationError

__version__ = "1.0.0"
__all__ = ["DeclarativeEnum", "DeclarativeEnumError", "PreprocessError", "ValidationError"]
