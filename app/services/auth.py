# app/services/auth.py
import hashlib
from app.models.user import User


class AuthService:
    @staticmethod
    def hash_password(password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def register(username, password, full_name=None):
        # Basic validation + create user
        if not username or not password:
            raise ValueError("username and password are required")
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters")
        existing = User.get_by_username(username)
        if existing:
            raise ValueError("username already exists")
        hashed_password = AuthService.hash_password(password)
        user_id = User.create(username, hashed_password, full_name)
        return user_id

    @staticmethod
    def login(username, password):
        if not username or not password:
            return False
        user = User.get_by_username(username)
        if not user:
            return False
        hashed_password = AuthService.hash_password(password)
        return user.password == hashed_password