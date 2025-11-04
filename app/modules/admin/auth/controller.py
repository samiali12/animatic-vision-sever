from fastapi import APIRouter, Depends, HTTPException, status
from modules.admin.auth.schemas import AdminLoginRequest, AdminRegisterRequest
from modules.admin.auth.service import AdminAuthService
from core.middleware import is_authenticated, get_refresh_token
from database.redis import redis_client
from datetime import datetime, UTC


router = APIRouter(prefix="/admin/auth", tags=["Admin Auth"])


def get_admin_auth_service():
    return AdminAuthService()


def assert_admin(user: dict):
    if (user or {}).get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )

@router.post("/register")
def admin_register(
    request: AdminRegisterRequest,
    service: AdminAuthService = Depends(get_admin_auth_service),
):
    return service.register(request)

@router.post("/login")
def admin_login(request: AdminLoginRequest, service: AdminAuthService = Depends(get_admin_auth_service)):
    return service.login(request.email, request.password)


@router.get("/me")
def admin_me(user: dict = Depends(is_authenticated), service: AdminAuthService = Depends(get_admin_auth_service)):
    assert_admin(user)
    return service.me(user["email"])


@router.post("/logout")
def admin_logout(user: dict = Depends(is_authenticated)):
    assert_admin(user)
    exp = user.get("exp")
    token = user.get("token")
    if exp:
        ttl = exp - int(datetime.now(UTC).timestamp())
        if ttl < 0:
            ttl = 0
        else:
            ttl = 900
    redis_client.setex(f"blacklist:{token}", ttl, "revoked")
    return {"message": f"Admin {user['email']} logged out successfully.", "status_code": 200}


@router.get("/refresh-token")
def admin_refresh_token(user: dict = Depends(get_refresh_token), service: AdminAuthService = Depends(get_admin_auth_service)):
    assert_admin(user)
    return service.generate_refresh_token(
        user["id"], user["fullName"], user["email"], user["role"], user["token"]
    )



