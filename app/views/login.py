# app/views/login.py
import tkinter as tk
from tkinter import messagebox
from app.services.auth import AuthService
from app.utils.style import center_window, make_button, make_header, apply_theme, THEME, card_frame
from tkinter import ttk


class LoginWindow:
    def __init__(self, master, on_success=None, on_register=None):
        self.master = master
        self.on_success = on_success
        self.on_register = on_register
        master.title("Hotel Booking - Login")
        center_window(master, 900, 600)
        apply_theme(master)

        # Main container
        container = tk.Frame(master, bg=THEME['bg'])
        container.pack(fill=tk.BOTH, expand=True)

        # Card in center for the login form
        card = card_frame(container, padx=28, pady=24)
        card.place(relx=0.5, rely=0.12, anchor='n')

        header = make_header(card.inner, "Welcome — Please sign in")
        header.pack(pady=(2, 12))

        form = tk.Frame(card.inner, bg=THEME['card_bg'])
        form.pack(padx=6, pady=6)

        ttk.Label(form, text="Username:", style='Muted.TLabel').grid(row=0, column=0, sticky='w', pady=(6, 2))
        self.username_entry = ttk.Entry(form, width=40)
        self.username_entry.grid(row=1, column=0, pady=(0, 8), ipady=6)

        ttk.Label(form, text="Password:", style='Muted.TLabel').grid(row=2, column=0, sticky='w', pady=(8, 2))
        self.password_entry = ttk.Entry(form, show='*', width=40)
        self.password_entry.grid(row=3, column=0, pady=(0, 10), ipady=6)
        self.password_entry.bind('<Return>', lambda e: self.handle_login())

        btn_frame = tk.Frame(card.inner, bg=THEME['card_bg'])
        btn_frame.pack(pady=(6, 2))

        # Primary login button
        login_btn = make_button(btn_frame, "Login", command=self.handle_login, width=20, variant='primary')
        login_btn.pack(pady=(6, 6))

        # Secondary create account button (styled)
        if self.on_register:
            create_btn = make_button(btn_frame, "Create Account", command=self.on_register, width=20, variant='secondary')
            create_btn.pack(pady=(2, 0))

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