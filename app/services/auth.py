# app/services/auth.py
from app.models.user import User


class AuthService:
@staticmethod
def register(username, password, full_name=None):
# Basic validation + create user
if not username or not password:
raise ValueError("username and password are required")
existing = User.get_by_username(username)
if existing:
raise ValueError("username already exists")
user_id = User.create(username, password, full_name)
return user_id


@staticmethod
def login(username, password):
if not username or not password:
return False
user = User.get_by_username(username)
if not user:
return False
return user.password == password