from ttkthemes import ThemedStyle
from tkcalendar import Calendar
from datetime import datetime
from tkinter import ttk
import tkinter as tk


class CalWindow:
    def __init__(self, date_widget):

        self.window = tk.Tk()
        self.window.configure(background="#f3f3f3")
        self.window.title("Select a Date")
        self.window.geometry("250x250")
        self.window.resizable(False, False)

        style = ThemedStyle(self.window)
        style.set_theme("vista")

        self.window.iconbitmap('favicon.ico')
        self.date_widget = date_widget

        today = datetime.now()
        self.cal = Calendar(self.window, selectmode='day')
        self.cal.place(x=0, y=0)

        # Add Button and Label
        ttk.Button(self.window, text="Get Date",
                   command=self.date_getter).place(x=85, y=200)

        self.window.mainloop()

    def date_getter(self):
        self.date_widget.set(datetime.strptime(self.cal.get_date(), "%d/%m/%Y").strftime("%d/%m/%Y"))
        self.window.destroy()
