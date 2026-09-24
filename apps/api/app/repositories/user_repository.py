from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        return self.db.scalar(statement)

    def get_by_id(self, user_id) -> User | None:
        statement = select(User).where(User.id == user_id)
        return self.db.scalar(statement)

    def create(
        self,
        *,
        name: str,
        email: str,
        password_hash: str,
        phone: str | None = None,
        date_of_birth=None,
        profile_photo_url: str | None = None,
    ) -> User:
        user = User(
            name=name,
            email=email,
            password_hash=password_hash,
            phone=phone,
            date_of_birth=date_of_birth,
            profile_photo_url=profile_photo_url,
        )

        self.db.add(user)
        self.db.flush()
        self.db.refresh(user)

        return user
