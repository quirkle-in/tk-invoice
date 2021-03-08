# Import Required Library 
from tkcalendar import Calendar 
from datetime import datetime
import tkinter as tk
import os


class CalWindow:
    def __init__(self):

        self.window = tk.Tk()
        self.window.configure(background = "#f3f3f3")
        self.window.title("Create an Invoice")
        self.window.geometry("400x400")
        self.window.resizable(False, True)

        self.invoice_data = {}

        self.val = tk.StringVar()

        today = datetime.now()
        self.m, self.d, self.y = int(today.strftime("%m")), int(today.strftime("%d")), int(today.strftime("%Y"))

        self.cal = Calendar(self.window, selectmode='day', year = self.y, month = self.m, day = self.d)
        self.cal.pack()

        # Add Button and Label 
        tk.Button(self.window, text = "Get Date", command = self.date_getter).pack() 

        self.window.mainloop()

    
    def date_getter(self):
        self.val = self.cal.get_date()
        os.chdir('gui/')
        with open('date.txt', 'a') as file:
            file.write(self.val)
            
        self.window.destroy()