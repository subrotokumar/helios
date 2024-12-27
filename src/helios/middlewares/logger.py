from ..schema import Request

def request_logger_middleware(request: Request):
    print(
f"""
| REQUEST | {request.request_method} {request.path}
|==========
""", end=""
    )
    if request.queries:
        print("| QUERIES")
        for key, value in request.queries.items():
            print(f"| {key}: {value}")
        print("|==========")
    if request.body:
        print("  ", end="")
        print(request.body)
        print("|==========")