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


uid = AuthService.register('alice', 'pwd123', 'Alice')
assert uid == 1


# stub get_by_username to return a DummyUser for login
monkeypatch.setattr(User, 'get_by_username', staticmethod(lambda u: DummyUser('alice', 'pwd123')))
assert AuthService.login('alice', 'pwd123') is True
assert AuthService.login('alice', 'wrong') is False