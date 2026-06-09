from pydantic import BaseModel


class LoginRequest(BaseModel):
    identifier: str   # username or email
    password: str


class TokenResponse(BaseModel):
    token: str
    token_type: str = "bearer"
