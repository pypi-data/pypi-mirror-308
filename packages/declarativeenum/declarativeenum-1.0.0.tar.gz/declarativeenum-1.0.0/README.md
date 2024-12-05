# DeclarativeEnum

A declarative and flexible approach to Python enums that supports preprocessing, validation, namespacing, and direct value access.

## Features

- Value preprocessing and validation
- Auto-numbering support
- Namespace prefixing
- Pattern formatting
- Value type enforcement
- Method chaining with direct access
- Aliases support

## Installation

```bash
pip install declarativeenum
```

## Basic Usage

```python
from declarativeenum import DeclarativeEnum

# Basic enum with direct string values
class Colors(DeclarativeEnum):
    RED
    BLUE
    GREEN

assert Colors.RED.value == "RED"

# Enum with preprocessing
class Headers(DeclarativeEnum):
    __preprocess__ = lambda x: f"X-Custom-{x.lower()}"
    TRACKING
    VERSION

assert Headers.TRACKING.value == "X-Custom-tracking"

# Enum with type conversion and validation
class Ports(DeclarativeEnum):
    __type__ = int
    __validate__ = lambda x: 0 <= x <= 65535
    HTTP = "80"
    HTTPS = "443"

assert isinstance(Ports.HTTP.value, int)
assert Ports.HTTPS.value == 443

# Enum with direct value access
class StatusCode(DeclarativeEnum):
    __directaccess__ = True
    OK = 200
    NOT_FOUND = 404

# Direct comparison works
assert StatusCode.OK == 200
```

## Advanced Features

### Preprocessing and Validation

```python
class ValidatedEnum(DeclarativeEnum):
    __preprocess__ = lambda x: x.upper()
    __validate__ = lambda x: len(x) <= 10
    __type__ = str

    SHORT
    ALSO_SHORT
```

### Pattern Formatting

```python
class APIEndpoints(DeclarativeEnum):
    __pattern__ = "/api/v1/{}"
    __namespace__ = "users"

    PROFILE  # becomes "/api/v1/users/profile"
    SETTINGS # becomes "/api/v1/users/settings"
```

### Auto-numbering

```python
class OrderedEnum(DeclarativeEnum):
    __autonumber__ = 100  # Start from 100
    FIRST   # 100
    SECOND  # 101
    THIRD   # 102
```

### Method Chaining with Direct Access

```python
class Headers(DeclarativeEnum):
    __directaccess__ = True
    CONTENT_TYPE = "application/json"

assert Headers.CONTENT_TYPE.upper() == "APPLICATION/JSON"
```

## License

MIT License - see LICENSE file for details.
