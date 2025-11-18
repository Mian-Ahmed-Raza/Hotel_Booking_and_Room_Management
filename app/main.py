# app/main.py
import tkinter as tk
from app.views.login import LoginWindow
from app.views.register import RegisterWindow
from app.views.dashboard import Dashboard
from app.models.user import User
from app.models.room import Room
from app.models.booking import Booking
from app.models.review import Review


def run_app():
    # Ensure all DB tables exist
    try:
        User.create_table()
        Room.create_table()
        Booking.create_table()
        Review.create_table()
        print("✓ All database tables initialized")
    except Exception as e:
        print(f"Warning: Could not create tables: {e}")

    root = tk.Tk()

    def open_dashboard():
        # destroy login window widgets and open dashboard
        for widget in root.winfo_children():
            widget.destroy()
        Dashboard(root)

    def open_login():
        # destroy current widgets and show login
        for widget in root.winfo_children():
            widget.destroy()
        LoginWindow(root, on_success=open_dashboard, on_register=open_register)

    def open_register():
        # destroy current widgets and show register
        for widget in root.winfo_children():
            widget.destroy()
        RegisterWindow(root, on_success=open_login)

    LoginWindow(root, on_success=open_dashboard, on_register=open_register)
    root.mainloop()




if __name__ == '__main__':
    run_app()