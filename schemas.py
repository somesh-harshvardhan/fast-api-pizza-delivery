from pydantic import BaseModel
from typing import Optional


class SignUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "john doe",
                "email": "john@gmail.com",
                "password": "password",
                "is_staff": False,
                "is_active": True,
            }
        }


class Settings(BaseModel):
    authjwt_secret_key: str = (
        "c24b08c6b5c00ddc5ccb82db6b809116b397025a9cadcaf68a34d9243cd0be8f"
    )


class LoginModel(BaseModel):
    username: str
    password: str
