# app/views/dashboard.py
import tkinter as tk
from tkinter import messagebox
from app.utils.style import center_window, make_button, make_header, apply_theme


class Dashboard:
    def __init__(self, master):
        self.master = master
        master.title("Hotel Management System - Dashboard")
        center_window(master, 900, 600)

        apply_theme(master)
        # Header
        header = make_header(master, "🏨 Hotel Management System")
        header.pack(pady=(18, 8))

        # Welcome message
        tk.Label(master, text="Welcome to the Dashboard", 
            font=('Segoe UI', 12), fg='#34495e', bg=master['bg']).pack(pady=6)
        
        # Create frame for buttons
        button_frame = tk.Frame(master)
        button_frame.pack(pady=20)
        
        # Grid layout for buttons
        buttons = [
            ("🛏️ Room Management", self.open_room_management, '#3498db'),
            ("📅 Booking Management", self.open_booking_management, '#9b59b6'),
            ("🔑 Check-in / Check-out", self.open_checkin_checkout, '#1abc9c'),
            ("💰 Billing & Invoices", self.open_billing, '#2ecc71'),
            ("⭐ Feedback & Reviews", self.open_feedback, '#f39c12'),
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            btn = make_button(button_frame, text, command=command, color=color, width=36, height=2)
            btn.pack(pady=8)
        
        # Stats frame (optional - shows quick stats)
        stats_frame = tk.Frame(master, relief=tk.RIDGE, borderwidth=2, bg='#ecf0f1')
        stats_frame.pack(pady=20, padx=50, fill=tk.X)
        
        tk.Label(stats_frame, text="Quick Stats", font=('Arial', 11, 'bold'), 
                bg='#ecf0f1').pack(pady=5)
        
        stats_text = tk.Label(stats_frame, 
                             text="Use the buttons above to manage your hotel operations",
                             font=('Arial', 9), bg='#ecf0f1', fg='#7f8c8d')
        stats_text.pack(pady=5)
        
        # Logout button
        make_button(master, "🚪 Logout", command=self.logout, color='#e74c3c', width=20).pack(pady=15)
    
    def open_room_management(self):
        from app.views.room_management import RoomManagementWindow
        window = tk.Toplevel(self.master)
        RoomManagementWindow(window)
    
    def open_booking_management(self):
        from app.views.booking_management import BookingManagementWindow
        window = tk.Toplevel(self.master)
        BookingManagementWindow(window)
    
    def open_checkin_checkout(self):
        from app.views.checkin_checkout import CheckInCheckOutWindow
        window = tk.Toplevel(self.master)
        CheckInCheckOutWindow(window)
    
    def open_billing(self):
        from app.views.billing import BillingWindow
        window = tk.Toplevel(self.master)
        BillingWindow(window)
    
    def open_feedback(self):
        from app.views.feedback import FeedbackWindow
        window = tk.Toplevel(self.master)
        FeedbackWindow(window)
    
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.master.quit()