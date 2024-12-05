# ~/DeclarativeEnum/src/declarativeenum/exceptions.py
class DeclarativeEnumError(Exception):
    """Base exception for DeclarativeEnum errors."""
    pass

class PreprocessError(DeclarativeEnumError):
    """Raised when preprocessing of an enum value fails."""
    pass

class ValidationError(DeclarativeEnumError):
    """Raised when enum value validation fails."""
    pass
