from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle
import tkinter as tk
import json
import os


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
        self.setting_variables = {}


        self.base_frame = ttk.Frame(self.window)
        self.base_frame.pack(padx = 10)

        self.canvas = tk.Canvas(self.base_frame, width=500, height = 600)
        self.scrollbar_y = ttk.Scrollbar(self.base_frame, #canvas, maybe
            orient = "vertical", command = self.canvas.yview)
        self.frame = ttk.Frame(self.canvas)

        self.frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion = self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.frame, anchor="n")
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar_y.pack(side="right", fill = "y")


        for setting in self.settings:
            self.setting_variables[setting] = tk.StringVar(self.window, value = self.settings[setting])
            
            f = ttk.Frame(self.frame)
            ttk.Label(f, text = setting.replace("_", " ").upper(), font = ("Arial", 10, "bold")).pack(side = tk.LEFT, padx = 10, pady = 30)
            entry = ttk.Entry(f, textvariable = self.setting_variables[setting],  width = 60)
            entry.pack(side = tk.RIGHT, expand = True, padx = 30, pady = 10)
            f.pack()



        self.btn_save = ttk.Button(self.window, text = "Save & Exit", command = self.save_and_exit)
        self.btn_save.pack(expand = True, padx = 20, pady = 10)


        self.window.mainloop()
    

    def save_settings(self):
        try:
            with open(file_path, 'w') as json_file:
                json.dump(self.settings, json_file)
            return True
        except Exception as e:
            print(e)
            return False
    
    def load_settings(self):
        with open(file_path, 'r') as json_file:
            self.settings = json.load(json_file)
            #print(self.settings)

    def save_and_exit(self):
        print("Saving settings...")
        if self.save_settings():
            print("Saved.")
            messagebox.showinfo("Success", "Settings saved.")
        else:
            print("Could not save.")
            messagebox.showinfo("Error", "Settings not saved.")
        self.window.destroy()

    