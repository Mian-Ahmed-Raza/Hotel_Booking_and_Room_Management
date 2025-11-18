# app/main.py
import tkinter as tk
from app.views.login import LoginWindow
from app.views.dashboard import Dashboard
from app.models.user import User




def run_app():
# Ensure DB table exists
User.create_table()


root = tk.Tk()


def open_dashboard():
# destroy login window widgets and open dashboard
for widget in root.winfo_children():
widget.destroy()
Dashboard(root)


LoginWindow(root, on_success=open_dashboard)
root.mainloop()




if __name__ == '__main__':
run_app()