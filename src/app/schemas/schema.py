from typing import Optional
from pydantic import BaseModel, Field


class PatchUserBody(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    first_name: Optional[str] = Field(None, min_length=3, max_length=50)
    last_name: Optional[str] = Field(None, min_length=3, max_length=50)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "anonymous",
                "first_name": "anonymous_first_name",
                "last_name": "anonymous_last_name",
            }
        }


class UserBody(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    first_name: str = Field(..., min_length=3, max_length=50)
    last_name: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=50)
    role: str = "user"

    class Config:
        json_schema_extra = {
            "example": {
                "username": "anonymous",
                "first_name": "anonymous_first_name",
                "last_name": "anonymous_last_name",
                "password": "password",
                "role": "user",
            }
        }


class UserResponse(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    role: str

    class Config:
        from_attributes = True


class ChangePasswordBody(BaseModel):
    password: str
    new_password: str = Field(..., min_length=6, max_length=50)

    class Config:
        json_schema_extra = {
            "example": {
                "password": "password",
                "new_password": "new_password",
            }
        }
