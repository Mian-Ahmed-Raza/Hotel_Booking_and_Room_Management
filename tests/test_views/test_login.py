# tests/test_views/test_login.py
import tkinter as tk
from app.views.login import LoginWindow


def test_login_window_creation(monkeypatch):
    root = tk.Tk()
    # monkeypatch AuthService.login so it doesn't touch DB
    monkeypatch = __import__('pytest').MonkeyPatch()
    monkeypatch.setenv('DB_NAME', 'test_db')
    
    login_window = LoginWindow(root)
    assert login_window.master == root
    
    root.destroy()
    assert True