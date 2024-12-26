import inspect
from typing import Any, Optional, Callable, Dict, List
import types
from parse import parse
from .schema import Request, Response
from .enum.method import Method, SUPPORTED_REQ_METHODS

Middlewares = List[Callable]

class Helios:
    def __init__(self, middlewares: Middlewares = []) -> None:
        self.routes: Dict[str, Dict[str, Callable]] = dict()
        self.routes_middleware: Dict[str, Dict[str, Middlewares]] = dict()
        self.middlewares = middlewares


    def __call__(self, environ, start_response) -> Any:
        response = Response()
        request = Request(environ)

        for middleware in self.middlewares:
            if isinstance(middleware, types.FunctionType):
                middleware(request)
            else: 
                raise ValueError("Only functions are allowes as middlewares")
            
        for path, handler_dict in self.routes.items():
            parsed_path = parse(path, environ["PATH_INFO"])

            for request_method, handler in handler_dict.items():

                if environ["REQUEST_METHOD"] == request_method and parsed_path:

                    route_mw_list = self.routes_middleware[path][request_method]

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
        def wrapper(handler: Callable) -> Callable:
            self.route_common(path, Method.GET, handler, middlewares)
        return wrapper

    def post(
        self, 
        path: Optional[str] = None, 
        middlewares: Middlewares = []
    ) -> Callable:
        def wrapper(handler: Callable) -> Callable:
            self.route_common(path, Method.POST, handler, middlewares)
        return wrapper

    def delete(
        self, 
        path: Optional[str] = None, 
        middlewares: Middlewares = []
    ) -> Callable:
        def wrapper(handler: Callable) -> Callable:
            self.route_common(path, Method.DELETE, handler, middlewares)
        return wrapper
    
    def put(
        self, 
        path: Optional[str] = None, 
        middlewares: Middlewares = []
    ) -> Callable:
        def wrapper(handler: Callable) -> Callable:
            self.route_common(path, Method.PUT, handler, middlewares)
        return wrapper
    

    def route(
        self,
        path: Optional[str] = None,
        middlewares: Middlewares = []
    ) -> Callable:
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
    