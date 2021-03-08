# Import Required Library 
from tkcalendar import Calendar 
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import os


class CalWindow:
    def __init__(self):

        self.window = tk.Tk()
        self.window.configure(background = "#f3f3f3")
        self.window.title("Create an Invoice")
        self.window.geometry("400x400")
        self.window.resizable(False, True)

        style = ThemedStyle(self.window)
        style.set_theme("vista")

        self.invoice_data = {}

        self.val = tk.StringVar()

        today = datetime.now()
        self.m, self.d, self.y = int(today.strftime("%m")), int(today.strftime("%d")), int(today.strftime("%Y"))

        self.cal = Calendar(self.window, selectmode='day', year = self.y, month = self.m, day = self.d)
        self.cal.pack()

        # Add Button and Label 
        ttk.Button(self.window, text = "Get Date", command = self.date_getter).pack() 

        self.window.mainloop()

    
    def date_getter(self):
        self.val = self.cal.get_date()
        with open('gui/date.txt', 'w') as file:
            file.write(self.val)
            
        self.window.destroy()