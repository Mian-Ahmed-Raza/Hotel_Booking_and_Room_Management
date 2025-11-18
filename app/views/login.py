# app/views/login.py
import tkinter as tk
from tkinter import messagebox
from app.services.auth import AuthService
from app.utils.style import center_window, make_button, make_header, apply_theme


class LoginWindow:
    def __init__(self, master, on_success=None, on_register=None):
        self.master = master
        self.on_success = on_success
        self.on_register = on_register
        master.title("Hotel Booking - Login")
        center_window(master, 460, 320)
        apply_theme(master)

        header = make_header(master, "Welcome — Please sign in")
        header.pack(pady=(18, 6))

        tk.Label(master, text="Username:", bg=master['bg']).pack(pady=(8, 3))
        self.username_entry = tk.Entry(master, width=36)
        self.username_entry.pack()

        tk.Label(master, text="Password:", bg=master['bg']).pack(pady=(10, 3))
        self.password_entry = tk.Entry(master, show='*', width=36)
        self.password_entry.pack()
        self.password_entry.bind('<Return>', lambda e: self.handle_login())

        make_button(master, "Login", command=self.handle_login, width=18).pack(pady=12)
        # Add register link
        if self.on_register:
            make_button(master, "Create Account", command=self.on_register, color='#9b59b6', width=18).pack(pady=4)

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