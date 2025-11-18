# app/views/dashboard.py
import tkinter as tk
from app.utils.style import center_window


class Dashboard:
def __init__(self, master):
self.master = master
master.title("Admin Dashboard")
center_window(master, 800, 500)


tk.Label(master, text="Welcome to Hotel Booking Dashboard", font=(None, 16)).pack(pady=20)
# Add buttons for Room Availability, Check-in/out etc.
tk.Button(master, text="Room Availability (placeholder)").pack(pady=5)
tk.Button(master, text="Check-in / Check-out (placeholder)").pack(pady=5)
tk.Button(master, text="Booking Management (placeholder)").pack(pady=5)
tk.Button(master, text="Billing (placeholder)").pack(pady=5)
tk.Button(master, text="Feedback & Reviews (placeholder)").pack(pady=5)