from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
        self.db = db

    def register(self, data: RegisterRequest):
        email = str(data.email).lower()

        existing_user = self.repository.get_by_email(email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists.",
            )

        password_hash = hash_password(data.password)

        try:
            user = self.repository.create(
                name=data.name.strip(),
                email=email,
                password_hash=password_hash,
                phone=data.phone,
                date_of_birth=data.date_of_birth,
                profile_photo_url=data.profile_photo_url,
            )

            self.db.commit()
            self.db.refresh(user)

        except IntegrityError:
            self.db.rollback()

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with the supplied information already exists.",
            )

        return user

    def authenticate(self, data: LoginRequest):
        email = str(data.email).lower()

        user = self.repository.get_by_email(email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        if not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This account is inactive.",
            )

        return user

    def create_tokens(self, user_id: UUID):
        return {
            "access_token": create_access_token(str(user_id)),
            "refresh_token": create_refresh_token(str(user_id)),
            "token_type": "bearer",
        }
