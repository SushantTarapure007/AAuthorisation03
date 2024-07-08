from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum
from pydantic import BaseModel

Base = declarative_base()

class Role(str, Enum):
    admin = "admin"
    user = "user"
    manager = "manager"

class Token(BaseModel):
    access_token: str
    token_type: str

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLAlchemyEnum(Role), nullable=False)
