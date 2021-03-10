from gui.invoice_generation import InvoiceForm
from gui.add_entity_page import AddEntityPage
from gui.view_data_page import ViewDataPage
from gui.settings_page import SettingsPage
from ttkthemes import ThemedStyle
from tkinter import ttk
import tkinter as tk


class MainWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.configure(background="#f3f3f3")
        self.window.title("Home")
        self.window.geometry("1200x700")
        self.window.resizable(True, True)

        style = ThemedStyle(self.window)
        style.set_theme("vista")

        self.btn_create_invoice = ttk.Button(
            self.window, text="Create Invoice",
            command=self.create_invoice_page,
            width = 30
        )
        self.btn_create_invoice.pack(expand=True)


        self.btn_view_invoices = ttk.Button(
            self.window, text="View Data",
            command = self.view_invoice_page,
            width = 30
        )
        self.btn_view_invoices.pack(expand=True)


        self.btn_add_entity = ttk.Button(
            self.window, text="Add Entity",
            command = self.add_entity_page,
            width = 30
        )
        self.btn_add_entity.pack(expand=True)

        self.btn_settings = ttk.Button(
            self.window, text="Settings",
            command = self.settings_page,
            width = 30
        )
        self.btn_settings.pack(expand=True)

        self.window.mainloop()


    def create_invoice_page(self):
        InvoiceForm()

    
    def view_invoice_page(self):
        ViewDataPage()


    def add_entity_page(self):
        AddEntityPage()
    
    def settings_page(self):
        SettingsPage()