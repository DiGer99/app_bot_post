from pydantic import BaseModel, EmailStr, Field
from pydantic_settings import BaseSettings


class PostSchema(BaseModel):
    header: str
    text: str


class UserSchema(BaseModel):
    login: str = Field(description="email")
    password: str = Field(
        min_length=8, max_length=20, description="Password from 8 to 20 characters"
    )


class Token(BaseModel):
    access_token: str
    token_type: str
