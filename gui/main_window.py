from gui.view_data_window import ViewInvoiceWindow
from gui.invoice_generation import InvoiceForm
from ttkthemes import ThemedStyle
from tkinter import ttk
import tkinter as tk


class MainWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.configure(background="#f3f3f3")
        self.window.title("Home")
        self.window.geometry("1000x600")
        self.window.resizable(False, False)

        style = ThemedStyle(self.window)
        style.set_theme("vista")

        self.btn_create_invoice = ttk.Button(
            self.window, text="Create an Invoice",
            command=self.create_invoice_page,
            width = 30
        )
        self.btn_create_invoice.pack(expand=True, )

        self.btn_view_invoices = ttk.Button(
            self.window, text="View Invoices",
            command = self.view_invoice_page,
            width = 30
        )
        self.btn_view_invoices.pack(expand=True)

        self.window.mainloop()


    def create_invoice_page(self):
        InvoiceForm()

    
    def view_invoice_page(self):
        ViewInvoiceWindow()
