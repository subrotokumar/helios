from enum import Enum

class HttpStatus(str, Enum):
    OK = "200 OK"
    CREATED = "201 Created"
    NO_CONTENT = "204 No Content"
    BAD_REQUEST = "400 Bad Request"
    UNAUTHORIZED = "401 Unauthorized"
    FORBIDDEN = "403 Forbidden"
    NOT_FOUND = "404 Not Found"
    INTERNAL_SERVER_ERROR = "500 Internal Server Error"
    NOT_IMPLEMENTED = "501 Not Implemented"
    SERVICE_UNAVAILABLE = "503 Service Unavailable"

    @classmethod
    def from_code(cls, code: int) -> "HttpStatus":
        try:
            return cls(f"{code} {cls._value2member_map_[code].name}") 
        except KeyError:
            return None