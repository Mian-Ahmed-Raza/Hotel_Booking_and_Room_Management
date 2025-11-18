# tests/test_services/test_auth.py
import pytest
from app.services.auth import AuthService
from app.models.user import User


class DummyUser:
    def __init__(self, username, password):
        self.username = username
        self.password = password


def test_register_and_login(monkeypatch):
    # stub User.get_by_username and User.create
    monkeypatch.setattr(User, 'get_by_username', staticmethod(lambda u: None))
    monkeypatch.setattr(User, 'create', staticmethod(lambda u, p, f=None: 1))

    uid = AuthService.register('alice', 'password123', 'Alice')
    assert uid == 1

    # stub get_by_username to return a DummyUser for login
    # Need to use hashed password for comparison
    hashed_pwd = AuthService.hash_password('password123')
    monkeypatch.setattr(User, 'get_by_username', staticmethod(lambda u: DummyUser('alice', hashed_pwd)))
    assert AuthService.login('alice', 'password123') is True
    assert AuthService.login('alice', 'wrong') is False


def test_register_validation():
    with pytest.raises(ValueError, match="username and password are required"):
        AuthService.register('', '')
    
    with pytest.raises(ValueError, match="Password must be at least 6 characters"):
        AuthService.register('user', '12345')