from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.auth_dependencies import get_user_from_refresh_token
from app.api.dependencies import get_db
from app.schemas.auth import (
    AuthResponse,
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.services.user_service import UserService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
):
    service = UserService(db)

    user = service.register(data)
    tokens = service.create_tokens(user.id)

    return {
        "user": user,
        "tokens": tokens,
    }


@router.post(
    "/login",
    response_model=AuthResponse,
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    service = UserService(db)

    user = service.authenticate(data)
    tokens = service.create_tokens(user.id)

    return {
        "user": user,
        "tokens": tokens,
    }


@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh(
    data: RefreshRequest,
    db: Session = Depends(get_db),
):
    user = get_user_from_refresh_token(
        data.refresh_token,
        db,
    )

    service = UserService(db)

    return service.create_tokens(user.id)
