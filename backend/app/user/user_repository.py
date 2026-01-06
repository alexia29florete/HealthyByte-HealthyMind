from typing import Optional
from ..extensions import db
from ..models import User

class UserRepository:
    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        return User.query.filter_by(email=email.lower().strip()).first()

    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        return User.query.get(user_id)

    @staticmethod
    def create(user: User) -> User:
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update() -> None:
        db.session.commit()
