from pydantic import BaseModel, EmailStr, Field


class AdminUserListQuery(BaseModel):
    q: str | None = None
    role: str | None = Field(default=None, pattern="^(admin|user)$")
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=10, ge=1, le=100)


class AdminCreateUserRequest(BaseModel):
    fullName: str
    email: EmailStr
    password: str
    role: str = Field(pattern="^(admin|user)$")


class AdminUpdateUserRequest(BaseModel):
    fullName: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    role: str | None = Field(default=None, pattern="^(admin|user)$")


class AdminUpdateUserRoleRequest(BaseModel):
    role: str = Field(pattern="^(admin|user)$")


class AdminUpdatePasswordRequest(BaseModel):
    password: str


