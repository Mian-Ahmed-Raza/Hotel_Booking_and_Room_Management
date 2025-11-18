# app/views/feedback.py
import tkinter as tk
from tkinter import ttk, messagebox
from app.models.review import Review
from app.models.booking import Booking
from app.utils.style import center_window


class FeedbackWindow:
    def __init__(self, master):
        self.master = master
        master.title("Feedback & Reviews")
        center_window(master, 1000, 600)
        
        # Top frame
        top_frame = tk.Frame(master)
        top_frame.pack(pady=10)
        
        tk.Label(top_frame, text="Guest Feedback & Reviews", font=('Arial', 16, 'bold')).pack()
        
        # Stats frame
        stats_frame = tk.Frame(master, relief=tk.RIDGE, borderwidth=2, bg='#ecf0f1')
        stats_frame.pack(pady=10, padx=10, fill=tk.X)
        
        try:
            avg_rating = Review.get_average_rating()
            total_reviews = len(Review.get_all())
        except:
            avg_rating = 0.0
            total_reviews = 0
        
        stats_left = tk.Frame(stats_frame, bg='#ecf0f1')
        stats_left.pack(side=tk.LEFT, padx=20, pady=10)
        tk.Label(stats_left, text="Average Rating:", font=('Arial', 11, 'bold'), bg='#ecf0f1').pack()
        tk.Label(stats_left, text=f"{'⭐' * int(avg_rating)} {avg_rating:.1f}/5.0", 
                font=('Arial', 14, 'bold'), fg='#f39c12', bg='#ecf0f1').pack()
        
        stats_right = tk.Frame(stats_frame, bg='#ecf0f1')
        stats_right.pack(side=tk.LEFT, padx=20, pady=10)
        tk.Label(stats_right, text="Total Reviews:", font=('Arial', 11, 'bold'), bg='#ecf0f1').pack()
        tk.Label(stats_right, text=str(total_reviews), font=('Arial', 14, 'bold'), fg='#3498db', bg='#ecf0f1').pack()
        
        # Button frame
        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Add Review", command=self.add_review, width=15, bg='green', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Delete Review", command=self.delete_review, width=15, bg='red', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Refresh", command=self.load_reviews, width=15).pack(side=tk.LEFT, padx=5)
        
        # Treeview for displaying reviews
        tree_frame = tk.Frame(master)
        tree_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create treeview
        self.tree = ttk.Treeview(tree_frame, columns=('ID', 'Booking', 'Guest', 'Rating', 'Comment', 'Date'), 
                                  show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        # Define columns
        self.tree.heading('ID', text='Review ID')
        self.tree.heading('Booking', text='Booking ID')
        self.tree.heading('Guest', text='Guest Name')
        self.tree.heading('Rating', text='Rating')
        self.tree.heading('Comment', text='Comment')
        self.tree.heading('Date', text='Date')
        
        self.tree.column('ID', width=80)
        self.tree.column('Booking', width=100)
        self.tree.column('Guest', width=150)
        self.tree.column('Rating', width=100)
        self.tree.column('Comment', width=350)
        self.tree.column('Date', width=150)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Load reviews
        self.load_reviews()
        
        # Back button
        tk.Button(master, text="Back to Dashboard", command=master.destroy, width=20).pack(pady=10)
    
    def load_reviews(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load reviews from database
        try:
            reviews = Review.get_all()
            for review in reviews:
                rating_stars = '⭐' * review.rating
                self.tree.insert('', tk.END, values=(
                    review.id,
                    review.booking_id,
                    review.guest_name,
                    f"{rating_stars} ({review.rating}/5)",
                    review.comment or '',
                    review.created_at
                ))
            
            # Update stats
            avg_rating = Review.get_average_rating()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load reviews: {str(e)}")
    
    def add_review(self):
        AddReviewDialog(self.master, self)
    
    def delete_review(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a review to delete")
            return
        
        item = self.tree.item(selected[0])
        review_id = item['values'][0]
        guest_name = item['values'][2]
        
        if messagebox.askyesno("Confirm Delete", f"Delete review from {guest_name}?"):
            try:
                Review.delete(review_id)
                messagebox.showinfo("Success", "Review deleted successfully")
                self.load_reviews()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete review: {str(e)}")


class AddReviewDialog:
    def __init__(self, parent, feedback_window):
        self.feedback_window = feedback_window
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Review")
        center_window(self.dialog, 450, 400)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Booking Selection
        tk.Label(self.dialog, text="Select Completed Booking:").pack(pady=(20, 5))
        self.booking_var = tk.StringVar()
        self.booking_combo = ttk.Combobox(self.dialog, textvariable=self.booking_var, width=40, state='readonly')
        self.booking_combo.pack()
        self.load_completed_bookings()
        
        # Guest Name
        tk.Label(self.dialog, text="Guest Name:").pack(pady=(15, 5))
        self.guest_name_entry = tk.Entry(self.dialog, width=42)
        self.guest_name_entry.pack()
        
        # Rating
        tk.Label(self.dialog, text="Rating:").pack(pady=(15, 5))
        rating_frame = tk.Frame(self.dialog)
        rating_frame.pack()
        
        self.rating_var = tk.IntVar(value=5)
        for i in range(1, 6):
            tk.Radiobutton(rating_frame, text=f"{'⭐' * i} ({i})", variable=self.rating_var, 
                          value=i, font=('Arial', 10)).pack(anchor='w')
        
        # Comment
        tk.Label(self.dialog, text="Comment:").pack(pady=(15, 5))
        self.comment_text = tk.Text(self.dialog, width=40, height=6)
        self.comment_text.pack()
        
        # Buttons
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=20)
        tk.Button(button_frame, text="Submit Review", command=self.save_review, 
                 width=15, bg='green', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=self.dialog.destroy, width=15).pack(side=tk.LEFT, padx=5)
        
        # Bind booking selection to auto-fill guest name
        self.booking_combo.bind('<<ComboboxSelected>>', self.on_booking_selected)
    
    def load_completed_bookings(self):
        try:
            bookings = Booking.get_all()
            completed = [b for b in bookings if b.status == 'Completed']
            booking_list = [f"Booking #{b.id} - {b.guest_name}" for b in completed]
            self.booking_combo['values'] = booking_list
            self.bookings = completed
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load bookings: {str(e)}")
    
    def on_booking_selected(self, event):
        index = self.booking_combo.current()
        if index >= 0:
            booking = self.bookings[index]
            self.guest_name_entry.delete(0, tk.END)
            self.guest_name_entry.insert(0, booking.guest_name)
    
    def save_review(self):
        if not self.booking_var.get():
            messagebox.showwarning("Warning", "Please select a booking")
            return
        
        guest_name = self.guest_name_entry.get().strip()
        if not guest_name:
            messagebox.showwarning("Warning", "Please enter guest name")
            return
        
        rating = self.rating_var.get()
        comment = self.comment_text.get("1.0", tk.END).strip()
        
        try:
            index = self.booking_combo.current()
            booking = self.bookings[index]
            
            Review.create(booking.id, guest_name, rating, comment)
            messagebox.showinfo("Success", "Review submitted successfully!")
            self.feedback_window.load_reviews()
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save review: {str(e)}")
