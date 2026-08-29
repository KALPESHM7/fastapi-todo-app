# this file is used to define the request and response to be shown  for the To-Do List App and will be validated using pydantic
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str
    password: str
class UserResponse(BaseModel):
    id: int
    username: str

class TaskCreate(BaseModel):
    title: str = Field(min_length=1,max_length=200)

class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool

    model_config = {
        "from_attributes": True
    }

class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200
    )

    completed: bool | None = None

class TaskReplace(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    completed: bool

class UserCreate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50
    )

    password: str = Field(
        min_length=8,
        max_length=128
    )

class UserResponse(BaseModel):
    id: int
    username: str

class LoginRequest(BaseModel):
    username: str
    password: str
class TokenResponse(BaseModel):
    access_token: str
    token_type: str