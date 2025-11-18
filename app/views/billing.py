# app/views/billing.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from app.models.booking import Booking
from app.models.room import Room
from app.utils.style import center_window


class BillingWindow:
    def __init__(self, master):
        self.master = master
        master.title("Billing & Invoices")
        center_window(master, 1000, 600)
        
        # Top frame
        top_frame = tk.Frame(master)
        top_frame.pack(pady=10)
        
        tk.Label(top_frame, text="Billing & Invoice Management", font=('Arial', 16, 'bold')).pack()
        
        # Filter frame
        filter_frame = tk.Frame(master)
        filter_frame.pack(pady=10)
        
        tk.Label(filter_frame, text="Filter:").pack(side=tk.LEFT, padx=5)
        self.filter_var = tk.StringVar(value='All')
        ttk.Combobox(filter_frame, textvariable=self.filter_var, width=15,
                     values=['All', 'Completed', 'Checked-in', 'Confirmed'], state='readonly').pack(side=tk.LEFT, padx=5)
        tk.Button(filter_frame, text="Apply Filter", command=self.load_bookings, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(filter_frame, text="Generate Invoice", command=self.generate_invoice, width=15, bg='green', fg='white').pack(side=tk.LEFT, padx=5)
        
        # Treeview for displaying bookings
        tree_frame = tk.Frame(master)
        tree_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create treeview
        self.tree = ttk.Treeview(tree_frame, columns=('ID', 'Guest', 'Room', 'Check-in', 'Check-out', 'Nights', 'Total', 'Status'), 
                                  show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        # Define columns
        self.tree.heading('ID', text='Invoice #')
        self.tree.heading('Guest', text='Guest Name')
        self.tree.heading('Room', text='Room')
        self.tree.heading('Check-in', text='Check-in')
        self.tree.heading('Check-out', text='Check-out')
        self.tree.heading('Nights', text='Nights')
        self.tree.heading('Total', text='Total Amount')
        self.tree.heading('Status', text='Status')
        
        self.tree.column('ID', width=80)
        self.tree.column('Guest', width=150)
        self.tree.column('Room', width=100)
        self.tree.column('Check-in', width=100)
        self.tree.column('Check-out', width=100)
        self.tree.column('Nights', width=80)
        self.tree.column('Total', width=120)
        self.tree.column('Status', width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Summary frame
        summary_frame = tk.Frame(master, relief=tk.RIDGE, borderwidth=2)
        summary_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(summary_frame, text="Summary:", font=('Arial', 12, 'bold')).pack(side=tk.LEFT, padx=10)
        self.total_bookings_label = tk.Label(summary_frame, text="Total Bookings: 0", font=('Arial', 10))
        self.total_bookings_label.pack(side=tk.LEFT, padx=20)
        self.total_revenue_label = tk.Label(summary_frame, text="Total Revenue: $0.00", font=('Arial', 10, 'bold'), fg='green')
        self.total_revenue_label.pack(side=tk.LEFT, padx=20)
        
        # Load bookings
        self.load_bookings()
        
        # Back button
        tk.Button(master, text="Back to Dashboard", command=master.destroy, width=20).pack(pady=10)
    
    def load_bookings(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        total_revenue = 0
        count = 0
        
        # Load bookings from database
        try:
            bookings = Booking.get_all()
            filter_status = self.filter_var.get()
            
            for booking in bookings:
                # Apply filter
                if filter_status != 'All' and booking.status != filter_status:
                    continue
                
                room = Room.get_by_id(booking.room_id)
                room_number = room.room_number if room else 'N/A'
                
                # Calculate nights
                checkin = booking.check_in if isinstance(booking.check_in, datetime.date) else datetime.strptime(str(booking.check_in), '%Y-%m-%d').date()
                checkout = booking.check_out if isinstance(booking.check_out, datetime.date) else datetime.strptime(str(booking.check_out), '%Y-%m-%d').date()
                nights = (checkout - checkin).days
                
                self.tree.insert('', tk.END, values=(
                    f"INV-{booking.id:04d}",
                    booking.guest_name,
                    room_number,
                    booking.check_in,
                    booking.check_out,
                    nights,
                    f"${booking.total_price:.2f}",
                    booking.status
                ))
                
                total_revenue += float(booking.total_price)
                count += 1
            
            # Update summary
            self.total_bookings_label.config(text=f"Total Bookings: {count}")
            self.total_revenue_label.config(text=f"Total Revenue: ${total_revenue:.2f}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load billing data: {str(e)}")
    
    def generate_invoice(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a booking to generate invoice")
            return
        
        item = self.tree.item(selected[0])
        invoice_id = item['values'][0]
        booking_id = int(invoice_id.split('-')[1])
        
        booking = Booking.get_by_id(booking_id)
        if booking:
            InvoiceDialog(self.master, booking)


class InvoiceDialog:
    def __init__(self, parent, booking):
        dialog = tk.Toplevel(parent)
        dialog.title(f"Invoice - INV-{booking.id:04d}")
        center_window(dialog, 500, 600)
        dialog.transient(parent)
        
        # Header
        header_frame = tk.Frame(dialog, bg='#2c3e50', height=80)
        header_frame.pack(fill=tk.X)
        tk.Label(header_frame, text="HOTEL BOOKING INVOICE", font=('Arial', 18, 'bold'), 
                bg='#2c3e50', fg='white').pack(pady=20)
        
        # Invoice details frame
        details_frame = tk.Frame(dialog, padx=20, pady=20)
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        # Invoice number and date
        tk.Label(details_frame, text=f"Invoice #: INV-{booking.id:04d}", 
                font=('Arial', 12, 'bold')).pack(anchor='w')
        tk.Label(details_frame, text=f"Date: {datetime.now().strftime('%Y-%m-%d')}", 
                font=('Arial', 10)).pack(anchor='w', pady=(0, 10))
        
        # Divider
        ttk.Separator(details_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Guest information
        tk.Label(details_frame, text="GUEST INFORMATION", 
                font=('Arial', 11, 'bold'), fg='#2c3e50').pack(anchor='w', pady=(10, 5))
        tk.Label(details_frame, text=f"Name: {booking.guest_name}", 
                font=('Arial', 10)).pack(anchor='w')
        tk.Label(details_frame, text=f"Phone: {booking.guest_phone}", 
                font=('Arial', 10)).pack(anchor='w', pady=(0, 10))
        
        # Booking information
        room = Room.get_by_id(booking.room_id)
        
        tk.Label(details_frame, text="BOOKING DETAILS", 
                font=('Arial', 11, 'bold'), fg='#2c3e50').pack(anchor='w', pady=(10, 5))
        tk.Label(details_frame, text=f"Room Number: {room.room_number if room else 'N/A'}", 
                font=('Arial', 10)).pack(anchor='w')
        tk.Label(details_frame, text=f"Room Type: {room.room_type if room else 'N/A'}", 
                font=('Arial', 10)).pack(anchor='w')
        tk.Label(details_frame, text=f"Check-in: {booking.check_in}", 
                font=('Arial', 10)).pack(anchor='w')
        tk.Label(details_frame, text=f"Check-out: {booking.check_out}", 
                font=('Arial', 10)).pack(anchor='w')
        
        # Calculate nights
        checkin = booking.check_in if isinstance(booking.check_in, datetime.date) else datetime.strptime(str(booking.check_in), '%Y-%m-%d').date()
        checkout = booking.check_out if isinstance(booking.check_out, datetime.date) else datetime.strptime(str(booking.check_out), '%Y-%m-%d').date()
        nights = (checkout - checkin).days
        
        tk.Label(details_frame, text=f"Number of Nights: {nights}", 
                font=('Arial', 10)).pack(anchor='w')
        tk.Label(details_frame, text=f"Rate per Night: ${room.price if room else 0:.2f}", 
                font=('Arial', 10)).pack(anchor='w', pady=(0, 10))
        
        # Divider
        ttk.Separator(details_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # Payment summary
        tk.Label(details_frame, text="PAYMENT SUMMARY", 
                font=('Arial', 11, 'bold'), fg='#2c3e50').pack(anchor='w', pady=(10, 5))
        
        subtotal = float(booking.total_price)
        tax = subtotal * 0.10  # 10% tax
        total = subtotal + tax
        
        tk.Label(details_frame, text=f"Subtotal: ${subtotal:.2f}", 
                font=('Arial', 10)).pack(anchor='w')
        tk.Label(details_frame, text=f"Tax (10%): ${tax:.2f}", 
                font=('Arial', 10)).pack(anchor='w')
        
        # Total in highlighted box
        total_frame = tk.Frame(details_frame, bg='#27ae60', padx=10, pady=5)
        total_frame.pack(fill='x', pady=10)
        tk.Label(total_frame, text=f"TOTAL AMOUNT: ${total:.2f}", 
                font=('Arial', 14, 'bold'), bg='#27ae60', fg='white').pack()
        
        tk.Label(details_frame, text=f"Status: {booking.status}", 
                font=('Arial', 10, 'bold'), 
                fg='green' if booking.status == 'Completed' else 'orange').pack(anchor='w', pady=(10, 5))
        
        # Buttons
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=15)
        tk.Button(button_frame, text="Print Invoice", command=lambda: self.print_invoice(booking), 
                 width=15, bg='blue', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Close", command=dialog.destroy, width=15).pack(side=tk.LEFT, padx=5)
    
    def print_invoice(self, booking):
        messagebox.showinfo("Print", f"Invoice INV-{booking.id:04d} sent to printer\n(Print functionality to be implemented)")