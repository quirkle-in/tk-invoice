from models import get_last_invoice
from gui.datepick import CalWindow
from gui.goods_table import Table
from ttkthemes import ThemedStyle
from models import createInvoice
from datetime import datetime
from pathlib import Path
from tkinter import ttk
import tkinter as tk
import os


class InvoiceForm:
    def __init__(self):

        self.window = tk.Tk()
        self.window.configure(background="#f3f3f3")
        self.window.title("Create an Invoice")
        self.window.geometry("1000x600")
        self.window.resizable(True, True)

        style = ThemedStyle(self.window)
        style.set_theme("vista")

        try:
            x = get_last_invoice()
            # print(x)
            if not x:
                return
            else:
                self.invoice_number_default = tk.IntVar(self.window)
                self.invoice_number_default.set(x)
            print(self.invoice_number_default)
        except Exception as e:
            print(e)
            self.window.destroy()
            return

        self.invoice_data = {}

        self.back_to_home = ttk.Button(
            self.window, text="Back",
            command=self.back_to_home_page
        )
        self.back_to_home.place(x=50, y=20)  # place(x = 100, y = 50)

        ''' DATE PICKER STRING VAR '''
        self.dating = tk.StringVar(self.window)
        self.dating.set(datetime.now().strftime("%d/%m/%Y"))

        ''' TAX INVOICE FORM '''

        ttk.Label(self.window, text="TAX INVOICE",
                  font=("Arial", 12, "bold")
                  ).place(x=490, y=20)

        ttk.Label(self.window, text="Invoice Number:").place(x=100, y=80)
        ttk.Label(self.window, text="Invoice Date:").place(x=100, y=100)
        ttk.Label(self.window, text="Reverse Charges:").place(x=100, y=120)
        ttk.Label(self.window, text="State:").place(x=100, y=140)
        ttk.Label(self.window, text="Code:").place(x=320, y=140)

        ttk.Label(self.window, text="BILL TO PARTY").place(x=740, y=60)
        ttk.Label(self.window, text="Name:").place(x=600, y=80)
        ttk.Label(self.window, text="Address:").place(x=600, y=100)
        ttk.Label(self.window, text="GSTIN Unique ID:").place(x=600, y=120)
        ttk.Label(self.window, text="State:").place(x=600, y=140)
        ttk.Label(self.window, text="State Code:").place(x=820, y=140)

        ''' GOODS FORM / LISTBOX '''

        ttk.Label(self.window, text="GOODS",
                  font=("Arial", 10, "bold")
                  ).place(x=500, y=180)

        ''' BOTTOM '''

        ttk.Label(self.window, text="Rs. in Words:").place(x=100, y=420)

        ttk.Label(self.window, text="AYURVEDIC PROP MEDICINE").place(
            x=100, y=460)
        ttk.Label(self.window, text="Bank Name:").place(x=100, y=480)
        ttk.Label(self.window, text="A/c No.:").place(x=100, y=500)
        ttk.Label(self.window, text="IFS Code:").place(x=100, y=520)

        ttk.Label(self.window, text="Total Before Tax:").place(x=600, y=420)
        ttk.Label(self.window, text="CGST@ 6%:").place(x=600, y=440)
        ttk.Label(self.window, text="SGST@ 6%:").place(x=600, y=460)
        ttk.Label(self.window, text="Total Tax Amount:").place(x=600, y=480)
        ttk.Label(self.window, text="Total After Tax Amount:").place(
            x=600, y=500)
        ttk.Label(self.window, text="GST on Reverse Charges:").place(
            x=600, y=520)

        ''' ENTRY WIDGETS '''

        ''' Purchase / Sale option '''
        self.typeVar = tk.IntVar()
        self.purchase_radio_button = tk.Radiobutton(
            self.window, text="Purchase", variable=self.typeVar, value=0)
        self.purchase_radio_button.place(x=250, y=20)

        self.sale_radio_button = ttk.Radiobutton(
            self.window, text="Sale", variable=self.typeVar, value=1)
        self.sale_radio_button.place(x=350, y=20)

        self.entry_invoice_no = ttk.Entry(
            self.window, text=self.invoice_number_default)
        self.entry_invoice_no.place(x=250, y=80)
        self.entry_invoice_date = ttk.Entry(
            self.window, textvariable=self.dating)  # date picker
        self.entry_invoice_date.place(x=250, y=100)
        self.entry_reverse_charges = ttk.Entry(self.window)
        self.entry_reverse_charges.place(x=250, y=120)
        self.entry_state = ttk.Entry(self.window)
        self.entry_state.place(x=150, y=140, width=150)
        self.entry_code = ttk.Entry(self.window)
        self.entry_code.place(x=360, y=140, width=50)

        self.entry_party_name = ttk.Entry(self.window)
        self.entry_party_name.place(x=750, y=80)
        self.entry_party_address = ttk.Entry(self.window)
        self.entry_party_address.place(x=750, y=100)
        self.entry_party_gstin = ttk.Entry(self.window)
        self.entry_party_gstin.place(x=750, y=120)
        self.entry_party_state = ttk.Entry(self.window)
        self.entry_party_state.place(x=650, y=140, width=150)
        self.entry_party_code = ttk.Entry(self.window)
        self.entry_party_code.place(x=900, y=140, width=50)

        self.entry_rs_in_words = ttk.Entry(self.window)
        self.entry_rs_in_words.place(x=250, y=420)
        self.entry_bank_name = ttk.Entry(self.window)
        self.entry_bank_name.place(x=250, y=480)
        self.entry_ac_no = ttk.Entry(self.window)
        self.entry_ac_no.place(x=250, y=500)
        self.entry_ifc_code = ttk.Entry(self.window)
        self.entry_ifc_code.place(x=250, y=520)

        self.entry_total_before_tax = ttk.Entry(self.window)
        self.entry_total_before_tax.place(x=750, y=420)
        self.entry_cgst = ttk.Entry(self.window)
        self.entry_cgst.place(x=750, y=440)
        self.entry_sgst = ttk.Entry(self.window)
        self.entry_sgst.place(x=750, y=460)
        self.entry_total_tax_amt = ttk.Entry(self.window)
        self.entry_total_tax_amt.place(x=750, y=480)
        self.entry_total_after_tax_amt = ttk.Entry(self.window)
        self.entry_total_after_tax_amt.place(x=750, y=500)
        self.entry_gst_reverse_charge = ttk.Entry(self.window)
        self.entry_gst_reverse_charge.place(x=750, y=520)

        '''Generating goods details'''
        self.entry_invoice_date.bind("<1>", self.calOpen)
        self.goods_table = Table(self.window)

        ''' Date refresher button '''
        btn_date_refresher = ttk.Button(
            self.window, text="Refresh", command=self.date_refresh)
        btn_date_refresher.place(x=390, y=98)

        self.btn_invoice_submit = ttk.Button(
            self.window, text="Submit", command=self.onSubmit)
        self.btn_invoice_submit.place(x=490, y=560)

        ''' Window Mainloop '''
        self.window.mainloop()

    def back_to_home_page(self):
        ''' confirmation '''
        try:
            os.remove("gui/date.txt")
        except:
            pass
        self.window.destroy()

    def calOpen(self, event):
        CalWindow()

    def date_refresh(self):
        date_val = ''
        if not Path('gui/date.txt').is_file():
            with open('gui/date.txt', 'w') as file:
                file.write(datetime.now().strftime("%d/%m/%Y"))

            with open('gui/date.txt', 'r') as file:
                date_val = file.read()
            print(date_val)
            self.dating.set(date_val)
        else:
            with open('gui/date.txt', 'r') as file:
                date_val = file.read()
            print(date_val)
            self.dating.set(date_val)

    def insertInvoice(self):

        resp = createInvoice(
            invoice_date=datetime.strptime(
                self.entry_invoice_date.get(), '%d/%m/%Y'),
            invoice_no=self.entry_invoice_no.get(),
            party_name=self.entry_party_name.get(),
            party_address=self.entry_party_address.get(),
            party_gst=self.entry_party_gstin.get(),
            party_state=self.entry_party_state.get(),
            party_state_code=self.entry_party_code.get(),
            total=self.entry_total_tax_amt.get(),
            total_cgst=self.entry_cgst.get(),
            total_sgst=self.entry_sgst.get(),
            purchase=self.typeVar.get()
        )
        return resp

    def insertDetails(self, inv_id):
        dets = self.goods_table.getGoodsDetails()
        print(dets)

    def performCaluclations(self):
        dets = self.goods_table.getGoodsDetails()
        j = 0
        total = 0
        for i in dets:
            if i['deet_id'] != '':
                i['total'] = 0
                i['total'] = int(i['qty']) * int(i['rate'])
                i['taxable_amount'] = int(i['total'] - int(i['discount']))
                total = total + i['taxable_amount']
                print(self.goods_table.entries[j])
                print(self.goods_table.entries[j]['total'].set(i['total']))
                self.goods_table.entries[j]['taxable_amount'].set(
                    int(i['total']) - int(i['discount']))
                j = j + 1
        self.entry_total_before_tax.insert(0, (total))
        self.entry_cgst.insert(0, (total * 0.06))
        self.entry_sgst.insert(0, (total * 0.06))
        self.entry_total_tax_amt.insert(0, (total * 0.12))
        self.entry_total_after_tax_amt.insert(0, (total + total * 0.12))

    def onConfirm(self):
        print('Confirmed')
        inv_id = self.insertInvoice()
        print(inv_id)

    def onSubmit(self):

        self.performCaluclations()
        self.btn_invoice_submit.config(text='Confirm', command=self.onConfirm)

        # self.window.destroy()
