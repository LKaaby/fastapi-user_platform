from pydantic import BaseModel, Field
from typing import Literal, Optional

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)

class UserCreate(UserBase):
    password: str = Field(...)
    role: Literal["user", "admin"] = "user"

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[Literal["user", "admin"]] = None

class UserOut(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ADD LOGIN SCHEMA
class UserLogin(BaseModel):
    username: str
    password: str