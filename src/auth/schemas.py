from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    user_id: str
    username: str
    name: str
    role: str
    hospital_id: str | None = None
    state: str | None = None
    district: str | None = None


class LoginResponse(BaseModel):
    success: bool
    message: str
    access_token: str | None = None
    token_type: str = "bearer"
    user: UserResponse | None = None