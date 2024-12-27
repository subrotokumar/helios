import inspect
import types
from parse import parse
from typing import Any, Optional, Callable, Dict, List
from .schema import Request, Response
from .enum.method import Method, SUPPORTED_REQ_METHODS

Middlewares = List[Callable]

class Helios:
    """
    A class representing a Helios web application.

    This class registers routes, handles requests, and applies middlewares.

    Attributes:
        routes: A dictionary mapping paths to HTTP method handlers.
        routes_middleware: A dictionary mapping paths to middlewares per HTTP method.
        middlewares: A list of global middlewares to apply to every request.
    """

    
    def __init__(
        self, 
        middlewares: Middlewares = [], 
    ) -> None:
        """
        Initialize the Helios application with optional global middlewares.
        
        Attributes:
            routes: A dictionary mapping paths to HTTP method handlers.
            routes_middleware: A dictionary mapping paths to middlewares per HTTP method.
            middlewares: A list of global middlewares to apply to every request.
        """
        self.routes: Dict[str, Dict[str, Callable]] = dict()
        self.routes_middleware: Dict[str, Dict[str, Middlewares]] = dict()
        self.middlewares = middlewares


    def __call__(self, environ: Dict[str, Any], start_response:Callable) -> Any:
        """
        Handle an incoming WSGI request, process middlewares, and route the request.
        
        Args:
            environ: The WSGI environment dictionary.
            start_response: The WSGI start response callable.
            
        Returns:
            The WSGI-compatible response.
        """
        response = Response()
        request = Request(environ)

        # Apply global middlewares
        for middleware in self.middlewares:
            if isinstance(middleware, types.FunctionType):
                middleware(request)
            else: 
                raise ValueError("Only functions are allowed as middlewares")
        
        # Route request to the appropriate handler
                raise ValueError("Only functions are allowes as middlewares")
            
        for path, handler_dict in self.routes.items():
            parsed_path = parse(path, environ["PATH_INFO"])

            for request_method, handler in handler_dict.items():

                if environ["REQUEST_METHOD"] == request_method and parsed_path:

                    route_mw_list = self.routes_middleware[path][request_method]
                    # Apply route-specific middlewares

                    for mw in route_mw_list:
                        if isinstance(mw, types.FunctionType):
                            mw(request)

                    handler(request, response, **parsed_path.named)
                    return response.as_wsgi(start_response)
        
                
        return response.as_wsgi(start_response)

    def route_common(
        self, 
        path: str, 
        method: str | Method, 
        handler: Callable, 
        middlewares: Middlewares
    ):
        """
        Register a new route with the specified path, method, handler, and middlewares.
        
        Args:
            path: The URL path for the route.
            method: The HTTP method for the route.
            handler: The function to handle requests to this route.
            middlewares: A list of middlewares specific to this route.
            
        Returns:
            The handler function.
        """
        path_name = path or f"/{handler.__name__}"

        if isinstance(method, Method):
            method = method.value
        if method not in SUPPORTED_REQ_METHODS:
            raise ValueError("Unsupported request method type")

        if path_name not in self.routes:
            self.routes[path_name] = {}
        else:
            if method in self.routes[path_name]:
                raise Exception(f"Duplicate handler path {path_name} present for Method {method}")
        
            
        self.routes[path_name][method] = handler

        if path_name not in self.routes_middleware:
            self.routes_middleware[path_name] = {}
        self.routes_middleware[path_name][method] = middlewares

        return handler

    def get(
        self, 
        path: Optional[str] = None, 
        middlewares: Middlewares = []
    ) -> Callable:
        """
        Decorator to register a GET route.
        
        Args:
            path: The URL path for the route.
            middlewares: A list of middlewares specific to this route.
            
        Returns:
            A decorator function that registers the handler.
        """
        def wrapper(handler: Callable) -> Callable:
            self.route_common(path, Method.GET, handler, middlewares)
        return wrapper

    def post(
        self, 
        path: Optional[str] = None, 
        middlewares: Middlewares = []
    ) -> Callable:
        """
        Decorator to register a POST route.
        
        Args:
            path: The URL path for the route.
            middlewares: A list of middlewares specific to this route.
            
        Returns:
            A decorator function that registers the handler.
        """
        def wrapper(handler: Callable) -> Callable:
            self.route_common(path, Method.POST, handler, middlewares)
        return wrapper

    def delete(
        self, 
        path: Optional[str] = None, 
        middlewares: Middlewares = []
    ) -> Callable:
        """
        Decorator to register a DELETE route.
        
        Args:
            path: The URL path for the route.
            middlewares: A list of middlewares specific to this route.
            
        Returns:
            A decorator function that registers the handler.
        """
        def wrapper(handler: Callable) -> Callable:
            self.route_common(path, Method.DELETE, handler, middlewares)
        return wrapper
    
    def put(
        self, 
        path: Optional[str] = None, 
        middlewares: Middlewares = []
    ) -> Callable:
        """
        Decorator to register a PUT route.
        
        Args:
            path: The URL path for the route.
            middlewares: A list of middlewares specific to this route.
            
        Returns:
            A decorator function that registers the handler.
        """
        def wrapper(handler: Callable) -> Callable:
            self.route_common(path, Method.PUT, handler, middlewares)
        return wrapper
    

    def route(
        self,
        path: Optional[str] = None,
        middlewares: Middlewares = []
    ) -> Callable:
        """
        Decorator to register routes for a class based on method names.
        
        Args:
            path: The base URL path for the class routes.
            middlewares: A list of middlewares specific to these routes.
            
        Returns:
            A decorator function that registers handlers for each method in the class.
        """
        def wrapper(handler) -> Callable:
            if isinstance(handler, type):
                class_members = inspect.getmembers(handler, lambda x: inspect.isfunction(x) and not (
                    x.__name__.startswith("__") and x.__name__.endswith("__")
                ) and x.__name__.upper() in SUPPORTED_REQ_METHODS)

                for fn_name, fn_handler in class_members:
                    self.route_common(
                        path=path or f"/{handler.__name__}", 
                        handler=fn_handler, 
                        method=fn_name.upper(),
                        middlewares=middlewares
                    )
            else:
                print("@routes can only be used for classes")

        return wrapper
