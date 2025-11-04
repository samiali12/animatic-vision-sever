import os
from fastapi.responses import JSONResponse
from modules.admin.auth.repository import AdminAuthRepository
from modules.admin.auth.schemas import AdminMeResponse, AdminRegisterRequest
from core.security import generate_token, generate_refresh_token
from core.response import ApiResponse
from core.security import verify_token
from core.security import password_hashing


class AdminAuthService:
    def __init__(self, repo: AdminAuthRepository = AdminAuthRepository()):
        self.repo = repo

    def login(self, email: str, password: str):
        user = self.repo.login_admin(email, password)
        access_token = generate_token(user.id, user.fullName, user.email, user.role)
        refresh_token = generate_refresh_token(
            user.id, user.fullName, user.email, user.role
        )
        response = JSONResponse(
            content={
                "message": "Admin login successfully",
                "status_code": 200,
                "data": {
                    "id": user.id,
                    "fullName": user.fullName,
                    "email": user.email,
                    "role": user.role.value,
                },
            }
        )
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False if os.getenv("ENVIROMENT") == "development" else True,
            samesite="lax" if os.getenv("ENVIROMENT") == "development" else "none",
            max_age=3600,
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False if os.getenv("ENVIROMENT") == "development" else True,
            samesite="lax" if os.getenv("ENVIROMENT") == "development" else "none",
            max_age=7 * 24 * 3600,
        )
        return response

    def me(self, email: str):
        user = self.repo.me_admin(email)
        if not user:
            return ApiResponse.error(message="Admin not found", status_code=404)
        data = AdminMeResponse(
            id=user.id, fullName=user.fullName, email=user.email, role=user.role.value
        )
        return ApiResponse(message="Admin data", status_code=200, data=data.model_dump())

    def generate_refresh_token(
        self,
        id: int,
        fullName: str,
        email: str,
        role: str,
        refresh_token: str,
    ):
        flag = verify_token(refresh_token)
        if flag:
            access_token = generate_token(id, fullName, email, role)
            new_refresh_token = generate_refresh_token(id, fullName, email, role)
            response = JSONResponse(
                content={
                    "message": "token generated successfully",
                    "status_code": 200,
                    "data": None,
                },
            )
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=False if os.getenv("ENVIROMENT") == "development" else True,
                samesite="lax" if os.getenv("ENVIROMENT") == "development" else "none",
                max_age=3600,
            )
            response.set_cookie(
                key="refresh_token",
                value=new_refresh_token,
                httponly=True,
                secure=False if os.getenv("ENVIROMENT") == "development" else True,
                samesite="lax" if os.getenv("ENVIROMENT") == "development" else "none",
                max_age=7 * 24 * 3600,
            )
            return response

    def register(self, data: AdminRegisterRequest):
        hash = password_hashing(data.password)
        user = self.repo.create_admin(data.fullName, data.email, hash)
        return ApiResponse(
            message="Admin created successfully",
            status_code=201,
            data={
                "id": user.id,
                "fullName": user.fullName,
                "email": user.email,
                "role": user.role.value,
            },
        )


