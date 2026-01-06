from typing import Dict, Any, Optional
from flask_jwt_extended import create_access_token
from ..extensions import bcrypt
from ..models import User
from ..utils.json_utils import dumps, loads
from .user_repository import UserRepository

class UserService:
    @staticmethod
    def signup(email: str, password: str, name: Optional[str] = None, dietary_preferences: Optional[Dict[str, Any]] = None) -> User:
        email_n = email.lower().strip()
        if not email_n or "@" not in email_n:
            raise ValueError("Invalid email.")
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters.")

        if UserRepository.get_by_email(email_n):
            raise ValueError("Email already registered.")

        pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(
            email=email_n,
            name=(name or "").strip() or None,
            password_hash=pw_hash,
            dietary_preferences=dumps(dietary_preferences or {})
        )
        return UserRepository.create(user)

    @staticmethod
    def login(email: str, password: str) -> str:
        email_n = email.lower().strip()
        user = UserRepository.get_by_email(email_n)
        if not user:
            raise ValueError("Invalid credentials.")
        if not bcrypt.check_password_hash(user.password_hash, password):
            raise ValueError("Invalid credentials.")

        token = create_access_token(identity=str(user.id))
        return token

    @staticmethod
    def get_profile(user_id: int) -> Dict[str, Any]:
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found.")
        return {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "dietary_preferences": loads(user.dietary_preferences, {}),
            "created_at": user.created_at.isoformat()
        }

    @staticmethod
    def update_profile(user_id: int, name: Optional[str], dietary_preferences: Optional[Dict[str, Any]]):
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found.")

        if name is not None:
            user.name = name.strip() or None
        if dietary_preferences is not None:
            user.dietary_preferences = dumps(dietary_preferences)

        UserRepository.update()
        return UserService.get_profile(user_id)
