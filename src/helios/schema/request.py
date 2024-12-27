from collections import defaultdict
import dataclasses
from typing import Dict, Any
import json


@dataclasses.dataclass
class Request:
    """
    A dataclass to represent an HTTP request.

    The class is initialized with a dictionary of environment variables
    from a WSGI server. It provides convenience methods to access the
    request method, query string, and body.

    Attributes:
        environ (dict): A dictionary of environment variables.
        queries (defaultdict): A dictionary of query string parameters.
        body (Any): The body of the request as a string or bytes.
    """


    def __init__(self, environ: Dict[str, Any]) -> None:
        """
        Initialize the class with a dictionary of environment variables.
        """
        self.environ = environ
        self.queries = defaultdict(str)
        self.body: Any = None
        self.headers: Dict[str, Any] = []

        # Set convenience attributes for the request method, query string,
        # and body.

        for key, value in environ.items():
            setattr(self, key.replace(".", "_").lower(), value)

        self.request_method: str = environ.get("REQUEST_METHOD", "")
        self.path: str = environ.get("PATH_INFO", "")

        self.__extract_headers(environ)
        self.__extract_queries(environ)
        self.__extract_body(environ)
    
    def __extract_headers(self, environ: Dict[str, Any]):
        headers = {
            key[5:].replace('_', '-'): value
            for key, value in environ.items()
            if key.startswith('HTTP_')
        }
        content_type = environ.get('CONTENT_TYPE', '')
        content_length = environ.get('CONTENT_LENGTH', '')

        if content_type:
            headers['Content-Type'] = content_type
        if content_length:
            headers['Content-Length'] = content_length
        
    def __extract_body(self, environ: Dict[str, Any]):
        if self.request_method in ['POST', 'PUT']:
            try:
                # Read the request body and decode it as a string.
                content_length = int(environ.get('CONTENT_LENGTH', 0))

                raw_body = environ['wsgi.input'].read(content_length)
                if environ.get('CONTENT_TYPE', "").split(';')[0] == 'application/json':
                    self.body = json.loads(raw_body.decode('utf-8'))
                else:
                    self.body = raw_body.decode('utf-8')

            except (ValueError, json.JSONDecodeError):
                # If the request body is invalid, set it to None.
                self.body = None
    
    def __extract_queries(self, environ: Dict[str, Any]):
        if environ.get("QUERY_STRING"):
            # Split the query string into key-value pairs and store them in
            # the queries dictionary.
            for query in environ["QUERY_STRING"].split("&"):
                if "=" in query:
                    query_key, query_val = query.split("=", 1)
                    self.queries[query_key] = query_val