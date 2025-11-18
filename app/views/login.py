# app/views/login.py
import tkinter as tk
from tkinter import messagebox
from app.services.auth import AuthService
from app.utils.style import center_window


class LoginWindow:
def __init__(self, master, on_success=None):
self.master = master
self.on_success = on_success
master.title("Hotel Booking - Login")
center_window(master, 420, 220)


tk.Label(master, text="Username:").pack(pady=(20, 5))
self.username_entry = tk.Entry(master)
self.username_entry.pack()


tk.Label(master, text="Password:").pack(pady=(10, 5))
self.password_entry = tk.Entry(master, show='*')
self.password_entry.pack()


tk.Button(master, text="Login", command=self.handle_login).pack(pady=15)


def handle_login(self):
username = self.username_entry.get().strip()
password = self.password_entry.get().strip()
if AuthService.login(username, password):
messagebox.showinfo("Login", "Login successful")
if self.on_success:
self.on_success()
else:
messagebox.showerror("Login", "Invalid credentials")