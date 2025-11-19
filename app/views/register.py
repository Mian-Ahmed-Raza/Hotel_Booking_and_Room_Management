# app/views/register.py
import tkinter as tk
from tkinter import messagebox
from app.services.auth import AuthService
from app.utils.style import center_window, make_button, make_header, apply_theme, THEME
from tkinter import ttk


class RegisterWindow:
    def __init__(self, master, on_success=None):
        self.master = master
        self.on_success = on_success
        master.title("Create Account")
        center_window(master, 460, 380)
        apply_theme(master)

        header = make_header(master, "Create your account")
        header.pack(pady=(18, 6))

        ttk.Label(master, text="Username:", style='Muted.TLabel').pack(pady=(10, 3), anchor='w')
        self.username_entry = ttk.Entry(master, width=40)
        self.username_entry.pack()

        ttk.Label(master, text="Full Name:", style='Muted.TLabel').pack(pady=(10, 3), anchor='w')
        self.fullname_entry = ttk.Entry(master, width=40)
        self.fullname_entry.pack()

        ttk.Label(master, text="Password:", style='Muted.TLabel').pack(pady=(10, 3), anchor='w')
        self.password_entry = ttk.Entry(master, show='*', width=40)
        self.password_entry.pack()

        ttk.Label(master, text="Confirm Password:", style='Muted.TLabel').pack(pady=(10, 3), anchor='w')
        self.confirm_password_entry = ttk.Entry(master, show='*', width=40)
        self.confirm_password_entry.pack()
        self.confirm_password_entry.bind('<Return>', lambda e: self.handle_register())

        make_button(master, "Register", command=self.handle_register, width=18, color='#2ecc71').pack(pady=14)

    def handle_register(self):
        username = self.username_entry.get().strip()
        fullname = self.fullname_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Register", "Username and password are required")
            return

        if password != confirm_password:
            messagebox.showerror("Register", "Passwords do not match")
            return

        try:
            AuthService.register(username, password, fullname)
            messagebox.showinfo("Register", "Registration successful! You can now login.")
            if self.on_success:
                self.on_success()
        except ValueError as e:
            messagebox.showerror("Register", str(e))
        except Exception as e:
            messagebox.showerror("Register", f"Registration failed: {str(e)}")
