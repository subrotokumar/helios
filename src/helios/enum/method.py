from enum import Enum

SUPPORTED_REQ_METHODS = { 
    "GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"
}

class Method(str, Enum):
    GET = "GET"
    HEAD = "HEAD"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    CONNECT = "CONNECT"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"
    PATCH = "PATCH"
    
    @classmethod
    def has_value(cls, value: str) -> bool:
        """
        Check if the given value exists in the enum.

        Args:
            value (str): The value to check.

        Returns:
            bool: True if the value exists in the enum, False otherwise.
        """
        return value in cls._value2member_map_

    @classmethod
    def list_methods(cls) -> list:
        """
        Get a list of all enum values.

        Returns:
            list: A list of all enum values.
        """
        return [method.value for method in cls]