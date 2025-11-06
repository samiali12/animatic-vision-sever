from core.response import ApiResponse
from core.security import password_hashing
from modules.admin.users.repository import AdminUserRepository
from modules.admin.users.schemas import (
    AdminCreateUserRequest,
    AdminUpdateUserRequest,
    AdminUserListQuery,
)


class AdminUserService:
    def __init__(self, repo: AdminUserRepository = AdminUserRepository()):
        self.repo = repo

    def list_users(self, query: AdminUserListQuery):
        users, total = self.repo.list_users(
            search=query.q, role=query.role, page=query.page, limit=query.limit
        )
        data = {
            "items": [
                {
                    "id": u.id,
                    "fullName": u.fullName,
                    "email": u.email,
                    "role": u.role.value,
                    "created_at": str(u.created_at),
                    "updated_at": str(u.updated_at),
                }
                for u in users
            ],
            "total": total,
            "page": query.page,
            "limit": query.limit,
        }
        return ApiResponse(message="Users fetched successfully", status_code=200, data=data)

    def get_user(self, user_id: int):
        u = self.repo.get_user(user_id)
        if not u:
            return ApiResponse(message="User not found", status_code=404)
        data = {
            "id": u.id,
            "fullName": u.fullName,
            "email": u.email,
            "role": u.role.value,
            "created_at": str(u.created_at),
            "updated_at": str(u.updated_at),
        }
        return ApiResponse(message="User fetched", status_code=200, data=data)

    def create_user(self, payload: AdminCreateUserRequest):
        password_hash = password_hashing(payload.password)
        u = self.repo.create_user(
            full_name=payload.fullName,
            email=payload.email,
            password_hash=password_hash,
            role=payload.role,
        )
        data = {
            "id": u.id,
            "fullName": u.fullName,
            "email": u.email,
            "role": u.role.value,
        }
        return ApiResponse(message="User created", status_code=201, data=data)

    def update_user(self, user_id: int, payload: AdminUpdateUserRequest):
        password_hash = None
        if payload.password is not None:
            password_hash = password_hashing(payload.password)
        u = self.repo.update_user(
            user_id=user_id,
            full_name=payload.fullName,
            email=payload.email,
            role=payload.role,
            password_hash=password_hash,
        )
        if not u:
            return ApiResponse(message="User not found", status_code=404)
        data = {
            "id": u.id,
            "fullName": u.fullName,
            "email": u.email,
            "role": u.role.value,
        }
        return ApiResponse(message="User updated", status_code=200, data=data)

    def update_user_role(self, user_id: int, role: str):
        u = self.repo.update_user_role(user_id, role)
        if not u:
            return ApiResponse(message="User not found", status_code=404)
        data = {"id": u.id, "role": u.role.value}
        return ApiResponse(message="Role updated", status_code=200, data=data)

    def update_user_password(self, user_id: int, password: str):
        password_hash = password_hashing(password)
        u = self.repo.update_user_password(user_id, password_hash)
        if not u:
            return ApiResponse(message="User not found", status_code=404)
        return ApiResponse(message="Password updated", status_code=200, data=None)

    def delete_user(self, user_id: int):
        deleted = self.repo.delete_user(user_id)
        if not deleted:
            return ApiResponse(message="User not found", status_code=404)
        return ApiResponse(message="User deleted", status_code=200, data=None)


