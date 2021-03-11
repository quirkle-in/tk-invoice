from gui.components.tkinter_custom_button import TkinterCustomButton
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
        self.window.geometry("400x400")
        self.window.resizable(True, True)

        style = ThemedStyle(self.window)
        style.set_theme("breeze")
  
        self.window.iconbitmap('favicon.ico')

        self.btn_create_invoice = TkinterCustomButton(text="Create Invoice", command = self.create_invoice_page, width = 200, 
                                    corner_radius=15, hover_color = '#960020', fg_color='#f72c58', text_font=('Avenir',13))
        self.btn_create_invoice.pack(expand=True)

        self.btn_add_entity = TkinterCustomButton(text="Add Entity", command = self.add_entity_page, width = 200, 
                                    corner_radius=15, hover_color = '#cc7a10', fg_color = "#ccab28", text_font=('Avenir',13))
        
        self.btn_add_entity.pack(expand=True)

        self.btn_view_invoices = TkinterCustomButton(text="View & Export Data", command = self.view_invoice_page, width = 200, 
                                    corner_radius=15, hover_color = '#4f86ff', fg_color='#6399ff', text_font=('Avenir',13))
        self.btn_view_invoices.pack(expand=True)


        self.btn_settings = TkinterCustomButton(text="Settings", command = self.settings_page, width = 200, 
                                    corner_radius=15, hover_color = '#005e50', fg_color='#00966e', text_font=('Avenir',13))
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
