# app/views/checkin_checkout.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from app.models.booking import Booking
from app.models.room import Room
from app.utils.style import center_window


class CheckInCheckOutWindow:
    def __init__(self, master):
        self.master = master
        master.title("Check-in / Check-out Management")
        center_window(master, 1000, 600)
        
        # Top frame for buttons
        top_frame = tk.Frame(master)
        top_frame.pack(pady=10)
        
        tk.Button(top_frame, text="Check-in", command=self.check_in, width=15, bg='green', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Check-out", command=self.check_out, width=15, bg='blue', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Refresh", command=self.load_bookings, width=15).pack(side=tk.LEFT, padx=5)
        
        # Treeview for displaying active bookings
        tree_frame = tk.Frame(master)
        tree_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create treeview
        self.tree = ttk.Treeview(tree_frame, columns=('ID', 'Guest', 'Phone', 'Room', 'Check-in', 'Check-out', 'Status'), 
                                  show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        # Define columns
        self.tree.heading('ID', text='Booking ID')
        self.tree.heading('Guest', text='Guest Name')
        self.tree.heading('Phone', text='Phone')
        self.tree.heading('Room', text='Room')
        self.tree.heading('Check-in', text='Check-in Date')
        self.tree.heading('Check-out', text='Check-out Date')
        self.tree.heading('Status', text='Status')
        
        self.tree.column('ID', width=80)
        self.tree.column('Guest', width=150)
        self.tree.column('Phone', width=120)
        self.tree.column('Room', width=100)
        self.tree.column('Check-in', width=120)
        self.tree.column('Check-out', width=120)
        self.tree.column('Status', width=120)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Instructions
        instructions = tk.Label(master, text="Select a booking and click Check-in or Check-out", 
                               font=('Arial', 10), fg='blue')
        instructions.pack(pady=5)
        
        # Load bookings
        self.load_bookings()
        
        # Back button
        tk.Button(master, text="Back to Dashboard", command=master.destroy, width=20).pack(pady=10)
    
    def load_bookings(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load active bookings from database
        try:
            bookings = Booking.get_active()
            for booking in bookings:
                room = Room.get_by_id(booking.room_id)
                room_number = room.room_number if room else 'N/A'
                
                self.tree.insert('', tk.END, values=(
                    booking.id,
                    booking.guest_name,
                    booking.guest_phone,
                    room_number,
                    booking.check_in,
                    booking.check_out,
                    booking.status
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load bookings: {str(e)}")
    
    def check_in(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a booking to check-in")
            return
        
        item = self.tree.item(selected[0])
        booking_id = item['values'][0]
        guest_name = item['values'][1]
        status = item['values'][6]
        
        if status == 'Checked-in':
            messagebox.showinfo("Info", "Guest is already checked in")
            return
        
        if messagebox.askyesno("Confirm Check-in", f"Check-in {guest_name}?"):
            try:
                booking = Booking.get_by_id(booking_id)
                
                # Check if check-in date is today or past
                today = datetime.now().date()
                checkin_date = booking.check_in if isinstance(booking.check_in, datetime.date) else datetime.strptime(str(booking.check_in), '%Y-%m-%d').date()
                
                if checkin_date > today:
                    messagebox.showwarning("Warning", f"Check-in date is {checkin_date}. Too early to check-in.")
                    return
                
                # Update booking status
                Booking.update(booking_id, status='Checked-in')
                
                # Update room status
                Room.update(booking.room_id, status='Occupied')
                
                messagebox.showinfo("Success", f"{guest_name} checked in successfully!")
                self.load_bookings()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to check-in: {str(e)}")
    
    def check_out(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a booking to check-out")
            return
        
        item = self.tree.item(selected[0])
        booking_id = item['values'][0]
        guest_name = item['values'][1]
        room_number = item['values'][3]
        status = item['values'][6]
        
        if status == 'Confirmed':
            messagebox.showwarning("Warning", "Guest needs to check-in first")
            return
        
        if status == 'Completed':
            messagebox.showinfo("Info", "Guest already checked out")
            return
        
        if messagebox.askyesno("Confirm Check-out", f"Check-out {guest_name} from Room {room_number}?"):
            try:
                booking = Booking.get_by_id(booking_id)
                
                # Update booking status
                Booking.update(booking_id, status='Completed')
                
                # Update room status to available
                Room.update(booking.room_id, status='Available')
                
                messagebox.showinfo("Success", f"{guest_name} checked out successfully!\nRoom {room_number} is now available.")
                self.load_bookings()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to check-out: {str(e)}")
