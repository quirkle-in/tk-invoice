import tkinter as tk
from models import createInvoice, createDetails
from gui.goods_table import Table
from gui.datepick import CalWindow
from datetime import datetime

import os

class InvoiceForm:
    def __init__(self):

        self.window = tk.Tk()
        self.window.configure(background="#f3f3f3")
        self.window.title("Create an Invoice")
        self.window.geometry("1000x600")
        self.window.resizable(False, True)

        self.invoice_data = {}

        self.back_to_home = tk.Button(
            self.window, text="Back",
            command=self.back_to_home_page
        )
        self.back_to_home.place(x=50, y=20)  # place(x = 100, y = 50)

        ''' DATE PICKER STRING VAR '''
        self.dating = tk.StringVar(self.window)

        ''' TAX INVOICE FORM '''

        tk.Label(self.window, text="TAX INVOICE").place(x=490, y=20)

        tk.Label(self.window, text="Invoice Number:").place(x=100, y=80)
        tk.Label(self.window, text="Invoice Date:").place(x=100, y=100)
        tk.Label(self.window, text="Reverse Charges:").place(x=100, y=120)
        tk.Label(self.window, text="State:").place(x=100, y=140)
        tk.Label(self.window, text="Code:").place(x=320, y=140)

        tk.Label(self.window, text="BILL TO PARTY").place(x=740, y=60)
        tk.Label(self.window, text="Name:").place(x=600, y=80)
        tk.Label(self.window, text="Address:").place(x=600, y=100)
        tk.Label(self.window, text="GSTIN Unique ID:").place(x=600, y=120)
        tk.Label(self.window, text="State:").place(x=600, y=140)
        tk.Label(self.window, text="State Code:").place(x=820, y=140)

        ''' GOODS FORM / LISTBOX '''

        tk.Label(self.window, text="GOODS").place(x=500, y=180)

        ''' BOTTOM '''

        tk.Label(self.window, text="Rs. in Words:").place(x=100, y=420)

        tk.Label(self.window, text="AYURVEDIC PROP MEDICINE").place(
            x=100, y=460)
        tk.Label(self.window, text="Bank Name:").place(x=100, y=480)
        tk.Label(self.window, text="A/c No.:").place(x=100, y=500)
        tk.Label(self.window, text="IFS Code:").place(x=100, y=520)

        tk.Label(self.window, text="Total Before Tax:").place(x=600, y=420)
        tk.Label(self.window, text="CGST@ 6%:").place(x=600, y=440)
        tk.Label(self.window, text="SGST@ 6%:").place(x=600, y=460)
        tk.Label(self.window, text="Total Tax Amount:").place(x=600, y=480)
        tk.Label(self.window, text="Total After Tax Amount:").place(
            x=600, y=500)
        tk.Label(self.window, text="GST on Reverse Charges:").place(
            x=600, y=520)

        ''' ENTRY WIDGETS '''

        self.entry_invoice_no = tk.Entry(self.window)
        self.entry_invoice_no.place(x=250, y=80)
        self.entry_invoice_date = tk.Entry(self.window, textvariable = self.dating) # date picker
        self.entry_invoice_date.place(x=250, y=100)
        self.entry_reverse_charges = tk.Entry(self.window)
        self.entry_reverse_charges.place(x=250, y=120)
        self.entry_state = tk.Entry(self.window)
        self.entry_state.place(x=150, y=140, width=150)
        self.entry_code = tk.Entry(self.window)
        self.entry_code.place(x=360, y=140, width=50)

        self.entry_party_name = tk.Entry(self.window)
        self.entry_party_name.place(x=750, y=80)
        self.entry_party_address = tk.Entry(self.window)
        self.entry_party_address.place(x=750, y=100)
        self.entry_party_gstin = tk.Entry(self.window)
        self.entry_party_gstin.place(x=750, y=120)
        self.entry_party_state = tk.Entry(self.window)
        self.entry_party_state.place(x=650, y=140, width=150)
        self.entry_party_code = tk.Entry(self.window)
        self.entry_party_code.place(x=900, y=140, width=50)

        self.entry_rs_in_words = tk.Entry(self.window)
        self.entry_rs_in_words.place(x=250, y=420)
        self.entry_bank_name = tk.Entry(self.window)
        self.entry_bank_name.place(x=250, y=480)
        self.entry_ac_no = tk.Entry(self.window)
        self.entry_ac_no.place(x=250, y=500)
        self.entry_ifc_code = tk.Entry(self.window)
        self.entry_ifc_code.place(x=250, y=520)

        self.entry_total_before_tax = tk.Entry(self.window)
        self.entry_total_before_tax.place(x=750, y=420)
        self.entry_cgst = tk.Entry(self.window)
        self.entry_cgst.place(x=750, y=440)
        self.entry_sgst = tk.Entry(self.window)
        self.entry_sgst.place(x=750, y=460)
        self.entry_total_tax_amt = tk.Entry(self.window)
        self.entry_total_tax_amt.place(x=750, y=480)
        self.entry_total_after_tax_amt = tk.Entry(self.window)
        self.entry_total_after_tax_amt.place(x=750, y=500)
        self.entry_gst_reverse_charge = tk.Entry(self.window)
        self.entry_gst_reverse_charge.place(x=750, y=520)

        '''Date Picker event binder'''
        self.entry_invoice_date.bind("<1>", self.calOpen)
        self.goods_table = Table(self.window)
        

        ''' Date refresher button '''
        btn_date_refresher = tk.Button(self.window, text = "Refresh", command=self.date_refresh)
        btn_date_refresher.place(x=390, y=98)

        self.dating.set('click ')
        btn_invoice_submit = tk.Button(
            self.window, text="Submit", command=self.onSubmit)
        btn_invoice_submit.place(x=490, y=560)
        
        ''' Window Mainloop '''
        self.window.mainloop()


    def back_to_home_page(self):
        ''' confirmation '''
        pass
        self.window.destroy()


    def create_invoice(self):
        ''' data validation '''
        pass
    

    def calOpen(self, event):
        CalWindow()


    def date_refresh(self):
        date_val = ''
        with open('date.txt', 'r') as file:
            date_val = file.read()
        print(date_val)
        self.dating.set(date_val)

    
    def insertInvoice(self):
        
        resp = createInvoice(
            invoice_date = self.entry_invoice_date.get(),
            party_name = self.entry_party_name.get(),
            party_address = self.entry_party_address.get(),
            party_gst = self.entry_party_gstin.get(),
            party_state = self.entry_party_state.get(),
            party_state_code = self.entry_party_code.get(),
            total = self.entry_total_tax_amt.get(),
            total_cgst = self.entry_cgst.get(),
            total_sgst = self.entry_sgst.get(),
            purchase = True
        )
        print(resp)


    def onSubmit(self):
        self.insertInvoice()
        self.goods_table.getGoodsDetails()

        #self.window.destroy()
