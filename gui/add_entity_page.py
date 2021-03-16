from ttkthemes import ThemedStyle
from tkinter import messagebox
from models import Entity
from tkinter import ttk
import tkinter as tk
import models


class AddEntityPage:
    def __init__(self, SETTINGS, main_window):
        self.SETTINGS = SETTINGS
        self.main_window = main_window
        
        self.window = tk.Tk()
        self.window.configure(background = "#f3f3f3")
        self.window.title("Add an Entity")
        self.window.geometry("1200x700")
        self.window.resizable(True, True)

        
        style = ThemedStyle(self.window)
        style.set_theme("breeze")

        self.window.iconbitmap('favicon.ico')

        self.data = {}
        self.titles = [column.key for column in Entity.__table__.columns]
        self.titles.remove('entity_id')

        self.header_frame = ttk.Frame(self.window)
        self.header_frame.pack(padx=10, pady=10, expand = True)

        ttk.Label(self.header_frame, text="ADD ENTITY", font = ("Arial", 14, "bold")).pack(padx = 10, pady=5)
        ttk.Button(self.header_frame, text = "Back", command = self.back_to_home).pack(padx = 10, pady = 5)
        
        self.base_frame = ttk.Frame(self.window)
        self.base_frame.pack(anchor="n", expand = True)

        for field in self.titles:
            self.data[field] = tk.StringVar(self.window)

            f = ttk.Frame(self.base_frame)
            ttk.Label(f, text = field.replace("_", " ").upper()).pack(side = tk.LEFT, padx = 10, pady = 5)
            en = ttk.Entry(f, width = 30, textvariable = self.data[field])
            en.pack(side = tk.RIGHT, padx = 10, pady = 5)
            f.pack(anchor="e", expand = True)

        ttk.Button(self.window, text = "Add Entity", command = self.add_entity, width = 30).pack(pady = 5, expand = True)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.window.mainloop()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?", master=self.window):
            self.main_window.destroy()
            self.window.destroy()

    def add_entity(self):
        data = {}
        for field in self.data:
            x = self.data[field].get()
            if x == "":
                messagebox.showerror(title = "Error", message = "Invalid / empty fields", master=self.window)
                return
            data[field] = x
        
        res = models.create_entity(data)
        #print(res)
        if res:
            messagebox.showinfo(title = "Success!", message = "Created entity", master=self.window)
            self.back_to_home()
        else:
            messagebox.showerror(title = "Failed", message = "Unable to create entity.", master=self.window)


    def back_to_home(self):
        self.window.destroy()
        self.main_window.update()
        self.main_window.deiconify()
