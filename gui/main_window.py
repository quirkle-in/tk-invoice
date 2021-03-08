from gui.invoice_generation import InvoiceForm
from gui.view_data_window import ViewInvoiceWindow
import tkinter as tk


class MainWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.configure(background="#f3f3f3")
        self.window.title("Home")
        self.window.geometry("1000x600")
        self.window.resizable(False, False)

        self.btn_create_invoice = tk.Button(
            self.window, text="Create an Invoice",
            command=self.create_invoice_page
        )
        self.btn_create_invoice.pack(expand=True)

        self.btn_view_invoices = tk.Button(
            self.window, text="View Invoices",
            command = self.view_invoice_page
        )
        self.btn_view_invoices.pack(expand=True)

        self.window.mainloop()

    def create_invoice_page(self):
        InvoiceForm()
    
    def view_invoice_page(self):
        ViewInvoiceWindow()
