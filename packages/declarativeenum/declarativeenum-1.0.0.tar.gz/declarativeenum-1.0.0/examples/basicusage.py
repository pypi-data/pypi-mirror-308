from declarativeenum import DeclarativeEnum

# Basic usage with automatic string values
class Colors(DeclarativeEnum):
    RED
    BLUE
    GREEN

print(Colors.RED.value)  # Prints: RED
print(list(Colors))  # Prints all enum members

# Using preprocessing
class Headers(DeclarativeEnum):
    __preprocess__ = lambda x: f"X-Custom-{x.lower()}"
    TRACKING
    VERSION

print(Headers.TRACKING.value)  # Prints: X-Custom-tracking

# Using type conversion and validation
class Ports(DeclarativeEnum):
    __type__ = int
    __validate__ = lambda x: 0 <= x <= 65535
    HTTP = "80"
    HTTPS = "443"

print(isinstance(Ports.HTTP.value, int))  # Prints: True
print(Ports.HTTPS.value)  # Prints: 443

# Using direct value access
class StatusCode(DeclarativeEnum):
    __directaccess__ = True
    OK = 200
    NOT_FOUND = 404

# Direct comparison works
print(StatusCode.OK == 200)  # Prints: True

# Using pattern formatting
class APIEndpoints(DeclarativeEnum):
    __pattern__ = "/api/v1/{}"
    __namespace__ = "users"

    PROFILE  # becomes "/api/v1/users/profile"
    SETTINGS # becomes "/api/v1/users/settings"

print(APIEndpoints.PROFILE.value)  # Prints: /api/v1/users/profile

if __name__ == "__main__":
    # Run through all examples
    print("Basic enum:", Colors.RED.value)
    print("Preprocessed enum:", Headers.TRACKING.value)
    print("Typed enum:", Ports.HTTP.value)
    print("Direct access enum:", StatusCode.OK == 200)
    print("Pattern formatted enum:", APIEndpoints.PROFILE.value)
