from ttkthemes import ThemedStyle
from tkinter import messagebox
from models import Entity
from tkinter import ttk
import tkinter as tk
import models


class AddEntityPage:
    def __init__(self):
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

        ttk.Button(self.window, text = "Back", command = self.back_to_home).pack(padx = 10, pady = 5)

        ttk.Label(self.window, text="ADD ENTITY", font = ("Arial", 14, "bold")).pack(expand = True, padx = 15)
        
        for field in self.titles:
            self.data[field] = tk.StringVar(self.window)

            f = ttk.Frame(self.window)
            ttk.Label(f, text = field.replace("_", " ").upper()).pack(side = tk.LEFT, padx = 10, pady = 5)
            en = ttk.Entry(f, width = 30, textvariable = self.data[field])
            en.pack(side = tk.RIGHT, padx = 10, pady = 5)
            f.pack(expand = True)

        ttk.Button(self.window, text = "Add Entity", command = self.add_entity, width = 30).pack(expand = True, pady = 10)

        self.window.mainloop()


    def add_entity(self):
        data = {}
        for field in self.data:
            x = self.data[field].get()
            if x == "":
                messagebox.showerror(title = "Error", message = "Invalid / empty fields")
                return
            data[field] = x
        
        res = models.create_entity(data)
        print(res)
        if res:
            messagebox.showinfo(title = "Success!", message = "Created entity", master=self.window)
            self.back_to_home()
        else:
            messagebox.showerror(title = "Failed", message = "Unable to create entity.", master=self.window)


    def back_to_home(self):
        self.window.destroy()