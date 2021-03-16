from gui.invoice_generation import InvoiceForm
from gui.add_entity_page import AddEntityPage
from gui.view_data_page import ViewDataPage
from gui.settings_page import SettingsPage
from ttkthemes import ThemedStyle
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import json


class MainWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window["background"]="#f3f3f3"
        self.window.title("Home")
        self.window.geometry("1200x700")
        self.window.resizable(True, True)
        
        self.SETTINGS = None
        self.get_and_set_settings()

        self.window.configure(bg='#e2e2e2')

        style = ThemedStyle(self.window)
        style.set_theme("breeze")
  
        self.window.iconbitmap('favicon.ico')

        ttk.Label(self.window, text=self.SETTINGS["pdf_title"], font=("Arial", 30, "bold")).pack(padx=60, expand=True)
        ttk.Label(self.window, text="Invoice Manager", font=("Arial", 24)).pack(padx=60)

        # self.btn_create_invoice = TkinterCustomButton(text="Create Invoice", command = self.create_invoice_page, width = 200, 
        #                             corner_radius=15, hover_color = '#960020', fg_color='#f72c58', text_font=('Avenir',13))
        # self.btn_create_invoice.pack(expand=True)

        # self.btn_add_entity = TkinterCustomButton(text="Add Entity", command = self.add_entity_page, width = 200, 
        #                             corner_radius=15, hover_color = '#cc7a10', fg_color = "#ccab28", text_font=('Avenir',13))
        
        # self.btn_add_entity.pack(expand=True)

        # self.btn_view_invoices = TkinterCustomButton(text="View & Export Data", command = self.view_invoice_page, width = 200, 
        #                             corner_radius=15, hover_color = '#4f86ff', fg_color='#6399ff', text_font=('Avenir',13))
        # self.btn_view_invoices.pack(expand=True)


        # self.btn_settings = TkinterCustomButton(text="Settings", command = self.settings_page, width = 200, 
        #                             corner_radius=15, hover_color = '#005e50', fg_color='#00966e', text_font=('Avenir',13))
        # self.btn_settings.pack(expand=True)

        self.btn_create_invoice = ttk.Button(text="Create Invoice", command = self.create_invoice_page, width=60)
        self.btn_create_invoice.pack(expand=True, padx=60)

        self.btn_add_entity = ttk.Button(text="Add Entity", command = self.add_entity_page, width=60)
        self.btn_add_entity.pack(expand=True, padx=60)

        self.btn_view_invoices = ttk.Button(text="View & Export Data", command = self.view_invoice_page, width=60)
        self.btn_view_invoices.pack(expand=True, padx=60)

        self.btn_settings = ttk.Button(text="Settings", command = self.settings_page, width=60)
        self.btn_settings.pack(expand=True, padx=60)
  
        self.window.lift()
        self.window.attributes('-topmost',True)
        self.window.after_idle(self.window.attributes,'-topmost', False)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.window.mainloop()
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?", master=self.window):
            self.window.destroy()

    def create_invoice_page(self):
        self.get_and_set_settings()
        self.window.withdraw()
        InvoiceForm(self.SETTINGS, self.window)

    
    def view_invoice_page(self):
        self.get_and_set_settings()
        self.window.withdraw()
        ViewDataPage(self.SETTINGS, self.window)


    def add_entity_page(self):
        self.get_and_set_settings()
        self.window.withdraw()
        AddEntityPage(self.SETTINGS, self.window)
    

    def settings_page(self):
        self.get_and_set_settings()
        self.window.withdraw()
        SettingsPage(self.SETTINGS, self.window)


    def get_and_set_settings(self):
        path = 'settings.json'
        with open(path) as f:
            self.SETTINGS = json.load(f)
            # print(self.SETTINGS)