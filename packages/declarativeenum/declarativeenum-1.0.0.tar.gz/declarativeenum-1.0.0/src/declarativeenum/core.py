# ~/DeclarativeEnum/src/declarativeenum/core.py
from enum import Enum, EnumMeta
import json
from loguru import logger as log

class EnumDict(dict):
    # Config attributes we expect
    CFGATTRS = {
        '__pattern__', '__type__', '__namespace__', '__validate__',
        '__processors__', '__preprocess__', '__auto_number__', '__aliases__'
    }

    # Built-in Python decorators and special methods we should never process
    STDSPECIAL = {
        'classmethod', 'staticmethod', 'property',
        '__module__', '__qualname__', '__doc__'
    }

    # Methods that should never be treated as enum members
    METHODS = {
        'tojson', 'todict', 'values', 'names',
        '__str__', '__repr__', '__iter__'
    }

    def __init__(self):
        super().__init__()
        self._member_names = []

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            #log.debug(f"__getitem__ attempt for key: {key}")
            if (key in self.STDSPECIAL or
                key in self.METHODS or
                key.startswith('__') or
                key in globals().get('__builtins__', {})):  # Prevent builtins like 'str' from becoming members
                raise
            if not key.startswith('_') or key in self.CFGATTRS:
                if key not in self._member_names:
                    #log.debug(f"Adding {key} to member names")
                    self._member_names.append(key)
                self[key] = key
                return key
            raise

    def __setitem__(self, key, value):
        #log.debug(f"Setting {key}={value} (type: {type(value)})")
        if (key not in self.STDSPECIAL and
            key not in self.METHODS and
            not key.startswith('_') and
            key not in globals().get('__builtins__', {})):
            if not callable(value):
                if key not in self._member_names:
                    self._member_names.append(key)
        super().__setitem__(key, value)

def stringproxy(methodname):
    """Creates a proxy method that delegates to the corresponding string method"""
    def proxy(self, *args, **kwargs):
        return getattr(str(self.value), methodname)(*args, **kwargs)
    return proxy


class DeclarativeMeta(EnumMeta):
    @classmethod
    def __prepare__(metacls, cls, bases):
        #log.debug("Preparing class dictionary")
        return EnumDict()

    def __new__(metacls, cls, bases, classdict):
        #log.debug(f"Creating new class with members: {classdict._member_names}")
        #log.debug(f"All dict items: {dict(classdict)}")

        # Get configuration with defaults
        cfgmatch = lambda x: classdict.get(f'__{x}__')
        cfgoptions = {'pattern', 'type', 'namespace', 'validate', 'processors',
                     'preprocess', 'autonumber', 'aliases', 'directaccess'}
        config = {k: cfgmatch(k) if k != 'processors' else cfgmatch(k) or [] for k in cfgoptions}
        config['aliases'] = config['aliases'] or {}

        # Add preprocess to processors if defined
        if config['preprocess']:
            config['processors'].insert(0, config['preprocess'])

        # Initialize counter for auto-numbering
        counter = None
        if config['autonumber'] is not None:
            counter = 0 if config['autonumber'] is True else int(config['autonumber'])

        # Create new dict for processed members
        members = EnumDict()

        # Process primary members first
        for name in classdict._member_names:
            try:
                val = classdict[name]
                #log.debug(f"Processing member {name} with initial value {val}")

                if config['pattern']:
                    val = config['pattern'].format(val) if isinstance(config['pattern'], str) else config['pattern'](val)

                if config['namespace']:
                    val = f"{config['namespace']}/{str(val).lower()}" if isinstance(val, (str, int)) else val

                # Process with processors
                if config['processors']:
                    for proc in config['processors']:
                        if callable(proc):
                            try:
                                if isinstance(proc, type(str.upper)):  # Check for unbound string method
                                    val = getattr(str(val), proc.__name__)()
                                else:
                                    val = proc(val)
                            except Exception as e:
                                #log.error(f"Processor failed for {name}: {e}")
                                raise ValueError(f"Processing failed for {name}: {str(e)}")
                if counter is not None:
                    val = counter
                    counter += 1

                if config['type']:
                    try:
                        if isinstance(val, type) and val == str:  # Special handling for str class
                            val = "str"
                        val = config['type'](val)
                    except Exception as e:
                        #log.error(f"Type conversion failed for {name}: {e}")
                        raise ValueError(f"Type conversion failed for {name}: {str(e)}")

                if config['validate'] and not config['validate'](val):
                    raise ValueError(f"Validation failed for {name}: {val}")

                members[name] = val
                #log.debug(f"Final processed value for {name}: {val}")

            except Exception as e:
                #log.error(f"Failed to process {name}: {str(e)}")
                raise ValueError(f"Failed to process {name}: {str(e)}")

        # Process aliases after all primary members are created
        for primary, aliases in config['aliases'].items():
            if primary in members:
                for alias in aliases:
                    members[alias] = members[primary]
                    if alias not in members._member_names:
                        members._member_names.append(alias)

        # If direct access is enabled, customize the enum's behavior
        if config.get('directaccess'):
            def __eq__(self, other):
                if isinstance(other, type(self)):
                    return self.value == other.value
                return self.value == other

            def __hash__(self):
                return hash(self.value)

            def __str__(self):
                return str(self.value)

            def __repr__(self):
                return f"{self.__class__.__name__}.{self.name}"

            def __int__(self):
                try:
                    return int(self.value)
                except (TypeError, ValueError):
                    raise ValueError(f"Cannot convert {self.value} to int")

            def __float__(self):
                try:
                    return float(self.value)
                except (TypeError, ValueError):
                    raise ValueError(f"Cannot convert {self.value} to float")

            def __add__(self, other):
                return self.value + other

            def __radd__(self, other):
                return other + self.value

            def __sub__(self, other):
                return self.value - other

            def __rsub__(self, other):
                return other - self.value

            def __mul__(self, other):
                return self.value * other

            def __rmul__(self, other):
                return other * self.value

            def __truediv__(self, other):
                return self.value / other

            def __rtruediv__(self, other):
                return other / self.value

            def __lt__(self, other):
                if isinstance(other, type(self)):
                    return self.value < other.value
                return self.value < other

            def __le__(self, other):
                if isinstance(other, type(self)):
                    return self.value <= other.value
                return self.value <= other

            def __gt__(self, other):
                if isinstance(other, type(self)):
                    return self.value > other.value
                return self.value > other

            def __ge__(self, other):
                if isinstance(other, type(self)):
                    return self.value >= other.value
                return self.value >= other

            # Add all basic methods to the class
            methods = {
                '__eq__': __eq__,
                '__hash__': __hash__,
                '__str__': __str__,
                '__repr__': __repr__,
                '__int__': __int__,
                '__float__': __float__,
                '__add__': __add__,
                '__radd__': __radd__,
                '__sub__': __sub__,
                '__rsub__': __rsub__,
                '__mul__': __mul__,
                '__rmul__': __rmul__,
                '__truediv__': __truediv__,
                '__rtruediv__': __rtruediv__,
                '__lt__': __lt__,
                '__le__': __le__,
                '__gt__': __gt__,
                '__ge__': __ge__,
            }

            # Add string method proxies for common string operations
            stringmethods = [
                'upper', 'lower', 'title', 'capitalize',
                'strip', 'lstrip', 'rstrip', 'center',
                'ljust', 'rjust', 'replace', 'split',
                'rsplit', 'join', 'format'
            ]

            for methodname in stringmethods:
                methods[methodname] = stringproxy(methodname)

            members.update(methods)

        # Copy methods and special attributes
        for key, val in classdict.items():
            if (key.startswith('__') or
                callable(val) or
                key in EnumDict.METHODS or
                key in EnumDict.STDSPECIAL):
                members[key] = val

        return super().__new__(metacls, cls, bases, members)

class DeclarativeEnum(Enum, metaclass=DeclarativeMeta):
    def tojson(self):
        return json.dumps(self.todict())

    def todict(self):
        return {'name': self.name, 'value': self.value}

    @classmethod
    def values(cls):
        return [member.value for member in cls]

    @classmethod
    def names(cls):
        return [member.name for member in cls]

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"
