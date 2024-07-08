from pydantic import BaseModel
from enum import Enum

class Role(str, Enum):
    admin = "admin"
    user = "user"
    manager = "manager"

class UserCreate(BaseModel):
    username: str
    password: str
    role: Role

class UserResponse(BaseModel):
    id: int
    username: str
    role: Role

    class Config:
        orm_mode = True
