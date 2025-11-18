# app/views/login.py
import tkinter as tk
from tkinter import messagebox
from app.services.auth import AuthService
from app.utils.style import center_window


class LoginWindow:
    def __init__(self, master, on_success=None, on_register=None):
        self.master = master
        self.on_success = on_success
        self.on_register = on_register
        master.title("Hotel Booking - Login")
        center_window(master, 420, 280)

        tk.Label(master, text="Username:").pack(pady=(20, 5))
        self.username_entry = tk.Entry(master, width=30)
        self.username_entry.pack()

        tk.Label(master, text="Password:").pack(pady=(10, 5))
        self.password_entry = tk.Entry(master, show='*', width=30)
        self.password_entry.pack()
        self.password_entry.bind('<Return>', lambda e: self.handle_login())

        tk.Button(master, text="Login", command=self.handle_login, width=15).pack(pady=10)
        
        # Add register button
        if self.on_register:
            tk.Button(master, text="Create Account", command=self.on_register, width=15, fg='blue').pack(pady=5)

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Login", "Please enter both username and password")
            return
            
        if AuthService.login(username, password):
            messagebox.showinfo("Login", "Login successful")
            if self.on_success:
                self.on_success()
        else:
            messagebox.showerror("Login", "Invalid credentials")