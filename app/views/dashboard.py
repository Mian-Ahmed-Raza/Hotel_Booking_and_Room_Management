# app/views/dashboard.py
import tkinter as tk
from app.utils.style import center_window


class Dashboard:
    def __init__(self, master):
        self.master = master
        master.title("Admin Dashboard")
        center_window(master, 800, 500)

        tk.Label(master, text="Welcome to Hotel Booking Dashboard", font=(None, 16, 'bold')).pack(pady=20)
        
        # Create frame for buttons
        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)
        
        # Add buttons for Room Availability, Check-in/out etc.
        tk.Button(button_frame, text="Room Availability (placeholder)", width=30).pack(pady=5)
        tk.Button(button_frame, text="Check-in / Check-out (placeholder)", width=30).pack(pady=5)
        tk.Button(button_frame, text="Booking Management (placeholder)", width=30).pack(pady=5)
        tk.Button(button_frame, text="Billing (placeholder)", width=30).pack(pady=5)
        tk.Button(button_frame, text="Feedback & Reviews (placeholder)", width=30).pack(pady=5)
        
        # Add logout button
        tk.Button(button_frame, text="Logout", command=master.quit, width=30, fg='red').pack(pady=20)