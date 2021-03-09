import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import os
import json

file_path = "settings.json"

class SettingsPage:
    def __init__(self):
        self.settings = {}

        self.window = tk.Tk()
        self.window.configure(background="#f3f3f3")
        self.window.title("Create Invoice")
        self.window.geometry("1200x700")
        self.window.resizable(True, True)

        style = ThemedStyle(self.window)
        style.set_theme("vista")

        self.base_frame = ttk.Frame(self.window)
        self.base_frame.pack(side = tk.BOTTOM, padx=20, pady=20)

        self.load_settings()


        self.window.mainloop()
    

    def save_settings(self):
        with open(file_path, 'w') as json_file:
            json.dump(self.settings, json_file)
    
    
    def load_settings(self):
        with open(file_path, 'r') as json_file:
            self.settings = json.load(json_file)
            #print(self.settings)