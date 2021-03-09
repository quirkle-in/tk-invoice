from ttkthemes import ThemedStyle
from tkcalendar import Calendar 
from datetime import datetime
from tkinter import ttk
import tkinter as tk


class CalWindow:
    def __init__(self, date_widget):

        self.window = tk.Tk()
        self.window.configure(background = "#f3f3f3")
        self.window.title("Date")
        self.window.geometry("250x250")
        self.window.resizable(False, True)

        style = ThemedStyle(self.window)
        style.set_theme("vista")
        self.date_widget = date_widget

        self.invoice_data = {}

        self.val = tk.StringVar()

        today = datetime.now()
        self.m, self.d, self.y = int(today.strftime("%m")), int(today.strftime("%d")), int(today.strftime("%Y"))

        self.cal = Calendar(self.window, selectmode='day', year = self.y, month = self.m, day = self.d)
        self.cal.pack()

        # Add Button and Label 
        ttk.Button(self.window, text = "Get Date", command = self.date_getter).pack() 

        self.window.mainloop()