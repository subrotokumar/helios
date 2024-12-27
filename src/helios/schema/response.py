import dataclasses
import re
from json import dumps
from typing import Any, Dict, List, Union, Tuple, Callable
from ..enum.status import HttpStatus


@dataclasses.dataclass
class Response:
    """
    Represents a response to be sent back to the client.

    Attributes:
        status_code: The HTTP status code of the response.
        text: The content of the response.
        headers: The headers of the response.
        template_extension: The extension of the templating system.
    """
    
    status_code: HttpStatus = HttpStatus.NOT_FOUND
    text: Union[str, Dict[str, Any], List[Any]] = "Route not found!"
    headers: List[Tuple[str, str]] = dataclasses.field(default_factory=list)
    template_extension: str = "html"

    def as_wsgi(
        self, 
        start_response: Callable
    ) -> List[bytes]:
        """
        Convert the response to a WSGI-compatible format.

        Args:
            start_response: The WSGI start_response function.

        Returns:
            The WSGI-compatible response.
        """
        status = self.status_code.value
        start_response(status, self.headers)
        return [self.text.encode("utf-8")]

    def status(
        self, 
        code: Union[HttpStatus, int]
    ) -> "Response":
        """
        Set the status code of the response.

        Args:
            code: The status code.

        Returns:
            The response object.
        """
        if isinstance(code, int):
            self.status_code = str(code)
        elif isinstance(code, HttpStatus):
            self.status_code = code
        else:
            raise ValueError("Status codes must be int or HttpStatus.")
        return self

    def send(
        self, 
        status: HttpStatus = HttpStatus.OK, 
        body: Union[str, List, Dict[str, Any]] = "",
    ) -> "Response":
        """
        Set the status code and content of the response.

        Args:
            status: The status code.
            body: The content of the response.

        Returns:
            The response object.
        """  
        self.status_code = status
        self.text = body if isinstance(body, str) else dumps(body)

        self.headers.append(("Content-Type", "application/json"))
        self.headers.append(("Content-Length", str(len(self.text))))

        return self

    def render(
        self, 
        template_name: str, 
        context: Dict[str, Any]
    ) -> "Response":
        """
        Render a template with the given context.

        Args:
            template_name: The name of the template.
            context: The context to pass to the template.

        Returns:
            The response object.
        """
        path = f"{template_name}.{self.template_extension}"
        try:
            with open(path, "r", encoding="utf-8") as fp:
                template = fp.read()

            for key, value in context.items():
                template = re.sub(r"{{\s*" + re.escape(key) + r"\s*}}", str(value), template)

            self.headers.append(("Content-Type", "text/html"))
            self.text = template
            self.status(HttpStatus.OK)
        except FileNotFoundError:
            self.status(HttpStatus.NOT_FOUND)
            self.text = f"Template '{template_name}' not found."
        return self