import dataclasses
import re
from typing import Any, Dict, List, Union, Self, Tuple
from ..enum.status import HttpStatus

@dataclasses.dataclass
class Response:
    def __init__(
        self, 
        status_code: HttpStatus = HttpStatus.NOT_FOUND,
        text: Union[str, List, Dict[str, Any]] = "Route not found!", 
        headers: List[Tuple[str, str]] = [], 
        template_extension = 'html'
    ):
        self.status_code = status_code
        self.text = text
        self.headers = headers
        self.template_extension = template_extension.lower()

    def as_wsgi(self, start_response, template_extension = 'html'):
        start_response(self.status_code.value, headers=self.headers)
        return [self.text.encode()]

    def status(self, code: HttpStatus | int) -> Self:
        if isinstance(code, int):
            self.status_code = HttpStatus.from_code(code)
        elif isinstance(code, HttpStatus):
            self.status_code = code
        else:
            raise ValueError("Status codes have to be either int or string")
        if self.text == "Route not found!":
            self.text = ""
        return self
    
    def send(self, status: HttpStatus | int = 200, text: Union[str, List, Dict[str, Any]] = ""):
        self.status(status)
        self.text = text if isinstance(text, str) else str(text)
    
    def render(self, template_name: str, context: Dict[str, Any]):
        path = f"{template_name}.html"
        with open(path) as fp:
            template = fp.read()

            for key, value in context.items():
                template = re.sub(r'{{\s*' + re.escape(key) + r'\s*}}', str(value), template)

        self.headers.append(('Content-Type', 'text/html'))
        self.text = template
        self.status(HttpStatus.OK)