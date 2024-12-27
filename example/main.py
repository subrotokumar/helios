from helios import Helios, Request, Response, HttpStatus
from helios.middlewares import request_logger_middleware
from typing import List
import uuid
from pydantic import BaseModel

class User(BaseModel):
    id: str
    name: str

    def __init__(self, name: str):
        super().__init__(id=str(uuid.uuid4()), name=name)

users: List[User] = [User(name="Subroto")]


app = Helios(middlewares=[request_logger_middleware])

@app.get(path="/health")
def health_check_api(request: Request, response: Response):
    response.send(
        status=HttpStatus.OK,
        body={"message": "Service is healthy"}
    )

@app.get(path="/users")
def list_users(request: Request, response: Response):
    response.send(
        status=HttpStatus.OK,
        body=[user.__dict__ for user in users]
    )

@app.post(path="/users")
def add_user(request: Request, response: Response):
    print(f"body {request.body}")
    print(type(request.body))
    new_user = User(name=request.body["name"])
    users.append(new_user)
    response.send(
        status=HttpStatus.CREATED,
        body=new_user.__dict__
    )

