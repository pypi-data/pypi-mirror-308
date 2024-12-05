# tests/test_declarative_enum.py
import pytest
from declarativeenum import DeclarativeEnum

def test_basic_enum():
    """Test basic enum creation without preprocessing"""
    class Colors(DeclarativeEnum):
        RED
        BLUE
        GREEN

    assert Colors.RED.value == "RED"
    assert Colors.BLUE.value == "BLUE"
    assert Colors.GREEN.value == "GREEN"

    assert Colors.values() == ["RED", "BLUE", "GREEN"]
    assert Colors.names() == ["RED", "BLUE", "GREEN"]

    assert str(Colors.RED) == "RED"
    assert repr(Colors.RED) == "Colors.RED"

def test_preprocess():
    """Test enum with preprocessing function"""
    class LowerColors(DeclarativeEnum):
        __preprocess__ = lambda x: x.lower()
        RED
        BLUE

    assert LowerColors.RED.value == "red"
    assert LowerColors.BLUE.value == "blue"

    class PrefixedColors(DeclarativeEnum):
        __preprocess__ = lambda x: f"COLOR_{x}"
        RED
        BLUE

    assert PrefixedColors.RED.value == "COLOR_RED"
    assert PrefixedColors.BLUE.value == "COLOR_BLUE"

def test_complex_preprocess():
    """Test enum with more complex preprocessing"""
    class HTTPStatus(DeclarativeEnum):
        __preprocess__ = lambda x: int(x.split('_')[-1])
        OK_200
        NOT_FOUND_404
        SERVER_ERROR_500

    assert HTTPStatus.OK_200.value == 200
    assert HTTPStatus.NOT_FOUND_404.value == 404
    assert HTTPStatus.SERVER_ERROR_500.value == 500

def test_invalid_preprocess():
    """Test that invalid preprocessing raises appropriate errors"""
    with pytest.raises(ValueError):
        class InvalidEnum(DeclarativeEnum):
            __preprocess__ = lambda x: int(x)
            VALID_123
            INVALID_TEXT

    with pytest.raises(ValueError):
        class InvalidEnum2(DeclarativeEnum):
            __preprocess__ = lambda x: 1/0
            ANY_VALUE

def test_iteration():
    """Test that enum can be iterated over"""
    class Numbers(DeclarativeEnum):
        ONE
        TWO
        THREE

    assert len(list(Numbers)) == 3
    assert set(member.name for member in Numbers) == {"ONE", "TWO", "THREE"}

def test_comparison():
    """Test enum member comparison"""
    class Status(DeclarativeEnum):
        PENDING
        COMPLETE

    assert Status.PENDING == Status.PENDING
    assert Status.PENDING != Status.COMPLETE
    assert Status.PENDING is Status.PENDING

def test_attributes():
    """Test that special attributes are preserved"""
    class SpecialEnum(DeclarativeEnum):
        __preprocess__ = lambda x: x.lower()
        __doc__ = "This is a special enum"
        __special_attr__ = "special"
        NORMAL
        VALUE

    assert SpecialEnum.__doc__ == "This is a special enum"
    assert SpecialEnum.__special_attr__ == "special"
    assert SpecialEnum.NORMAL.value == "normal"

def test_pattern():
    """Test pattern formatting feature"""
    class Headers(DeclarativeEnum):
        __pattern__ = "X-Custom-{}"
        TRACKING
        VERSION

    assert Headers.TRACKING.value == "X-Custom-TRACKING"
    assert Headers.VERSION.value == "X-Custom-VERSION"

def test_types():
    """Test value type conversion"""
    class Ports(DeclarativeEnum):
        __type__ = int
        HTTP = "80"
        HTTPS = "443"

    assert isinstance(Ports.HTTP.value, int)
    assert Ports.HTTP.value == 80
    assert Ports.HTTPS.value == 443

def test_namespace():
    """Test namespace support"""
    class APIEndpoints(DeclarativeEnum):
        __namespace__ = "api/v1"
        USERS
        POSTS

    assert APIEndpoints.USERS.value == "api/v1/users"
    assert APIEndpoints.POSTS.value == "api/v1/posts"

def test_validate():
    """Test value validation"""
    class ValidatedEnum(DeclarativeEnum):
        __validate__ = lambda x: x.isalpha()
        VALID

    with pytest.raises(ValueError):
        class InvalidEnum(DeclarativeEnum):
            __validate__ = lambda x: x.isalpha()
            INVALID2

def test_process():
    """Test multiple processing steps"""
    class ComplexEnum(DeclarativeEnum):
        __processors__ = [
            str.upper,
            lambda x: f"PREFIX_{x}",
            lambda x: x.replace("_", "-")
        ]
        hello_world

    assert ComplexEnum.hello_world.value == "PREFIX-HELLO-WORLD"

def test_autonumber():
    """Test auto-numbering feature"""
    class NumberedEnum(DeclarativeEnum):
        __autonumber__ = 100
        FIRST
        SECOND
        THIRD

    assert NumberedEnum.FIRST.value == 100
    assert NumberedEnum.SECOND.value == 101
    assert NumberedEnum.THIRD.value == 102

def test_alias():
    """Test value aliases"""
    class Status(DeclarativeEnum):
        __aliases__ = {
            'OK': ['SUCCESS', 'COMPLETED'],
            'ERROR': ['FAILED', 'EXCEPTION']
        }
        OK = 200
        ERROR = 500

    assert Status.OK.value == 200
    assert Status.SUCCESS.value == 200
    assert Status.COMPLETED.value == 200
    assert Status.ERROR.value == 500
    assert Status.FAILED.value == 500

def test_serialize():
    """Test serialization methods"""
    class Simple(DeclarativeEnum):
        OK = 200

    assert Simple.OK.tojson() == '{"name": "OK", "value": 200}'
    assert Simple.OK.todict() == {'name': 'OK', 'value': 200}


def test_direct_access():
    """Test direct value access feature"""
    class Headers(DeclarativeEnum):
        __directaccess__ = True
        CONTENT_TYPE = "application/json"
        ACCEPT = "text/plain"

    # Direct comparisons
    assert Headers.CONTENT_TYPE == "application/json"
    assert Headers.ACCEPT == "text/plain"

    # Still works with .value
    assert Headers.CONTENT_TYPE.value == "application/json"

    # Works with type conversion for numeric values
    class Ports(DeclarativeEnum):
        __directaccess__ = True
        __type__ = int
        HTTP = "80"
        HTTPS = "443"

    assert Ports.HTTP == 80
    assert int(Ports.HTTPS) == 443

    # Works with string operations
    assert str(Headers.CONTENT_TYPE) == "application/json"
    assert Headers.CONTENT_TYPE.upper() == "APPLICATION/JSON"

    # Dictionary keys
    d = {Headers.CONTENT_TYPE: "value"}
    assert d[Headers.CONTENT_TYPE] == "value"
    assert d["application/json"] == "value"
