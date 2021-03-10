import models
from pdf_generation.create_invoice_pdf import create_invoice_pdf
from gui.settings_page import SettingsPage
from gui.add_entity_page import AddEntityPage
from gui.invoice_generation import InvoiceForm
from gui.view_data_page import ViewDataPage
from ttkthemes import ThemedStyle
from tkinter import ttk
import tkinter as tk


class MainWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.configure(background="#f3f3f3")
        self.window.title("Home")
        self.window.geometry("1000x600")
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
        
        self.btn_pdf = ttk.Button(
            self.window, text="PDF",
            command = self.temp_create_pdf,
            width = 30
        )
        self.btn_pdf.pack(expand=True)


        self.window.mainloop()


    def create_invoice_page(self):
        InvoiceForm()

    
    def view_invoice_page(self):
        ViewDataPage()


    def add_entity_page(self):
        AddEntityPage()
    
    def settings_page(self):
        SettingsPage()
    
    def temp_create_pdf(self):
        invoice, details = models.get_invoice_by_id(1)
        print(invoice, details)
        if invoice and details:
            invoice = {field : invoice.__dict__[field] for field in invoice.__dict__ }
            details = [{
                field : detail.__dict__[field] for field in detail.__dict__ 
            } for detail in details]
        
            create_invoice_pdf(invoice, details)