from fastapi import APIRouter, Depends, HTTPException, status
from core.middleware import is_authenticated
from modules.admin.users.schemas import (
    AdminCreateUserRequest,
    AdminUpdateUserRequest,
    AdminUpdateUserRoleRequest,
    AdminUpdatePasswordRequest,
    AdminUserListQuery,
)
from modules.admin.users.service import AdminUserService


router = APIRouter(prefix="/admin/users", tags=["Admin Users"])


def get_service():
    return AdminUserService()


def assert_admin(user: dict):
    if (user or {}).get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )


@router.get("")
def list_users(
    query: AdminUserListQuery = Depends(),
    user: dict = Depends(is_authenticated),
    service: AdminUserService = Depends(get_service),
):
    assert_admin(user)
    return service.list_users(query)


@router.get("/{user_id}")
def get_user(
    user_id: int,
    user: dict = Depends(is_authenticated),
    service: AdminUserService = Depends(get_service),
):
    assert_admin(user)
    return service.get_user(user_id)


@router.post("")
def create_user(
    payload: AdminCreateUserRequest,
    user: dict = Depends(is_authenticated),
    service: AdminUserService = Depends(get_service),
):
    assert_admin(user)
    return service.create_user(payload)


@router.put("/{user_id}")
def update_user(
    user_id: int,
    payload: AdminUpdateUserRequest,
    user: dict = Depends(is_authenticated),
    service: AdminUserService = Depends(get_service),
):
    assert_admin(user)
    return service.update_user(user_id, payload)


@router.patch("/{user_id}/role")
def update_user_role(
    user_id: int,
    payload: AdminUpdateUserRoleRequest,
    user: dict = Depends(is_authenticated),
    service: AdminUserService = Depends(get_service),
):
    assert_admin(user)
    return service.update_user_role(user_id, payload.role)


@router.patch("/{user_id}/password")
def update_user_password(
    user_id: int,
    payload: AdminUpdatePasswordRequest,
    user: dict = Depends(is_authenticated),
    service: AdminUserService = Depends(get_service),
):
    assert_admin(user)
    return service.update_user_password(user_id, payload.password)


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    user: dict = Depends(is_authenticated),
    service: AdminUserService = Depends(get_service),
):
    assert_admin(user)
    return service.delete_user(user_id)


