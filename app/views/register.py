# app/views/register.py
import tkinter as tk
from tkinter import messagebox
from app.services.auth import AuthService
from app.utils.style import center_window


class RegisterWindow:
    def __init__(self, master, on_success=None):
        self.master = master
        self.on_success = on_success
        master.title("Hotel Booking - Register")
        center_window(master, 420, 300)

        tk.Label(master, text="Username:").pack(pady=(20, 5))
        self.username_entry = tk.Entry(master, width=30)
        self.username_entry.pack()

        tk.Label(master, text="Full Name:").pack(pady=(10, 5))
        self.fullname_entry = tk.Entry(master, width=30)
        self.fullname_entry.pack()

        tk.Label(master, text="Password:").pack(pady=(10, 5))
        self.password_entry = tk.Entry(master, show='*', width=30)
        self.password_entry.pack()

        tk.Label(master, text="Confirm Password:").pack(pady=(10, 5))
        self.confirm_password_entry = tk.Entry(master, show='*', width=30)
        self.confirm_password_entry.pack()
        self.confirm_password_entry.bind('<Return>', lambda e: self.handle_register())

        tk.Button(master, text="Register", command=self.handle_register, width=15).pack(pady=15)

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
