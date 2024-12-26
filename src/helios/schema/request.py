from collections import defaultdict
import dataclasses
from typing import Dict, Any

@dataclasses.dataclass
class Request:
    def __init__(self, environ: Dict[str, Any]) -> None:
        self.queries = defaultdict()
        for key, value in environ.items():
            setattr(self, key.replace(".", "_").lower(), value)

        if self.query_string:
            req_queries = self.query_string.split("&")
            for query in req_queries:
               query_key, query_val = query.split("=")
               self.queries[query_key] = query_val 
