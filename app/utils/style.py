# app/utils/style.py
import tkinter as tk


def center_window(window, width=400, height=300):
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width - width) / 2)
y = int((screen_height - height) / 2)
window.geometry(f"{width}x{height}+{x}+{y}")\n
def make_label(master, text, **kwargs):
return tk.Label(master, text=text, **kwargs)