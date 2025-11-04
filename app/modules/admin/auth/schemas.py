from pydantic import BaseModel, EmailStr


class AdminLoginRequest(BaseModel):
    email: EmailStr
    password: str


class AdminMeResponse(BaseModel):
    id: int
    fullName: str
    email: EmailStr
    role: str


class AdminRegisterRequest(BaseModel):
    fullName: str
    email: EmailStr
    password: str


