from logging import error, exception
from re import T
from models import get_last_invoice, createDetails
from gui.datepick import CalWindow
from gui.goods_table import Table
from ttkthemes import ThemedStyle
from models import createInvoice
from tkinter import messagebox
from datetime import datetime
from pathlib import Path
from tkinter import ttk
from tkinter import END
import tkinter as tk
from pathlib import Path
from tkinter.scrolledtext import ScrolledText
import models
from tkinter import filedialog
from num2words import num2words

from pdf_generation import create_invoice_pdf


CAL_CLICKED = 0


class InvoiceForm:
    def __init__(self):

        self.window = tk.Tk()
        self.window.configure(background="#f3f3f3")
        self.window.title("Create Invoice")
        self.window.geometry("1200x760")
        self.window.resizable(False, False)

        style = ThemedStyle(self.window)
        style.set_theme("vista")

        try:
            x = get_last_invoice()
            if not x:
                return
            else:
                self.invoice_number_default = tk.IntVar(self.window)
                self.invoice_number_default.set(x)
        except Exception as e:
            print(e)
            self.window.destroy()
            return

        self.invoice_data = {}

        self.header_frame = ttk.Frame(self.window)
        self.header_frame.pack(expand = True, padx = 10, pady = 10)

        self.back_to_home = ttk.Button(
            self.header_frame, text="Back",
            command=self.back_to_home_page
        )
        self.back_to_home.grid(row = 0, column = 0, padx = 10, pady = 10)

        ''' DATE PICKER STRING VAR '''
        self.dating = tk.StringVar(self.window)
        self.dating.set(datetime.now().strftime("%d/%m/%Y"))

        ''' TAX INVOICE FORM '''


        ttk.Label(self.header_frame, text="TAX INVOICE",
                  font=("Arial", 13, "bold")
                  ).grid(row = 0, column = 1, padx = 10, pady = 10)
        

        # -
        self.top_frame = ttk.Frame(self.window)
        self.top_frame.pack(side = tk.TOP, expand=True, anchor="n")

        # - -
        self.top_left_frame = ttk.Frame(self.top_frame)
        self.top_left_frame.pack(side = tk.LEFT, anchor="n")

        # - - -
        self.top_left_subleft_frame = ttk.Frame(self.top_left_frame)
        self.top_left_subleft_frame.pack(side = tk.LEFT, anchor="s")
        
        # - - -
        self.top_left_subright_frame = ttk.Frame(self.top_left_frame)
        self.top_left_subright_frame.pack(side = tk.RIGHT, anchor="s")

        # - -
        self.top_right_frame = ttk.Frame(self.top_frame)
        self.top_right_frame.pack(side = tk.RIGHT, anchor="n")

        # - - -
        self.top_right_subleft_frame = ttk.Frame(self.top_right_frame)
        self.top_right_subleft_frame.pack(side = tk.LEFT, anchor="s")
        
        # - - -
        self.top_right_subright_frame = ttk.Frame(self.top_right_frame)
        self.top_right_subright_frame.pack(side = tk.RIGHT, anchor="s")


        ttk.Label(self.top_left_subleft_frame, text="Invoice Number:").grid(row = 0, column = 0, padx = 10, pady = 10)
        ttk.Label(self.top_left_subleft_frame, text="Invoice Date:").grid(row = 1, column = 0, padx = 10, pady = 10)
        ttk.Label(self.top_left_subleft_frame, text="Reverse Charges:").grid(row = 2, column = 0, padx = 10, pady = 10)
        ttk.Label(self.top_left_subleft_frame, text="State:").grid(row = 3, column = 0, padx = 10, pady = 10)
        ttk.Label(self.top_left_subleft_frame, text="Code:").grid(row = 4, column = 0, padx = 10, pady = 10)

        ttk.Label(self.top_right_subleft_frame, text="BILL TO PARTY").grid(row = 0, column = 0, padx = 10, pady = 10)
        ttk.Label(self.top_right_subleft_frame, text="Name:").grid(row = 1, column = 0, padx = 10, pady = 10)
        ttk.Label(self.top_right_subleft_frame, text="Address:").grid(row = 2, column = 0, padx = 10, pady = 10)
        ttk.Label(self.top_right_subleft_frame, text="GSTIN Unique ID:").grid(row = 3, column = 0, padx = 10, pady = 10)
        ttk.Label(self.top_right_subleft_frame, text="State:").grid(row = 4, column = 0, padx = 10, pady = 10)
        ttk.Label(self.top_right_subleft_frame, text="State Code:").grid(row = 5, column = 0, padx = 10, pady = 10)

        ''' GOODS FORM / LISTBOX '''

        ttk.Label(self.window, text="GOODS",
                  font=("Arial", 11, "bold")
                  ).pack(expand = True)
        
        
        self.footer_frame = ttk.Frame(self.window)
        self.footer_frame.pack(side = tk.BOTTOM)

        ''' BOTTOM '''

        # -
        self.bottom_frame = ttk.Frame(self.window)
        self.bottom_frame.pack(side = tk.BOTTOM, expand = True, anchor="n")

        # - -
        self.bottom_left_frame = ttk.Frame(self.bottom_frame)
        self.bottom_left_frame.pack(side = tk.LEFT, anchor="n")
        
        # - - -
        self.bottom_left_subleft_frame = ttk.Frame(self.bottom_left_frame)
        self.bottom_left_subleft_frame.pack(side = tk.LEFT, anchor="n")
        
        # - - -
        self.bottom_left_subright_frame = ttk.Frame(self.bottom_left_frame)
        self.bottom_left_subright_frame.pack(side = tk.RIGHT, anchor="n")
        
        # - -
        self.bottom_right_frame = ttk.Frame(self.bottom_frame)
        self.bottom_right_frame.pack(side = tk.RIGHT, anchor="n")
        
        # - - -
        self.bottom_right_subleft_frame = ttk.Frame(self.bottom_right_frame)
        self.bottom_right_subleft_frame.pack(side = tk.LEFT, anchor="n")
        
        # - - -
        self.bottom_right_subright_frame = ttk.Frame(self.bottom_right_frame)
        self.bottom_right_subright_frame.pack(side = tk.RIGHT, anchor="n")

        ttk.Label(self.bottom_left_subleft_frame, text="Rs. in Words:").grid(row = 1, column = 0, padx = 10, pady = 10)

        #ttk.Label(self.bottom_left_subleft_frame, text="AYURVEDIC PROP MEDICINE").grid(row = 2, column = 0, padx = 10, pady = 10)
        ttk.Label(self.bottom_left_subleft_frame, text="Bank Name:").grid(row = 3, column = 0, padx = 10, pady = 10)
        ttk.Label(self.bottom_left_subleft_frame, text="A/c No.:").grid(row = 4, column = 0, padx = 10, pady = 10)
        ttk.Label(self.bottom_left_subleft_frame, text="IFS Code:").grid(row = 5, column = 0, padx = 10, pady = 10)

        ttk.Label(self.bottom_right_subleft_frame, text="Total Before Tax:").grid(row = 0, column = 0, padx = 10, pady = 10)
        ttk.Label(self.bottom_right_subleft_frame, text="IGST:").grid(row = 1, column = 0, padx = 10, pady = 10)
        ttk.Label(self.bottom_right_subleft_frame, text="CGST@ 6%:").grid(row = 2, column = 0, padx = 10, pady = 10)
        ttk.Label(self.bottom_right_subleft_frame, text="SGST@ 6%:").grid(row = 3, column = 0, padx = 10, pady = 10)
        ttk.Label(self.bottom_right_subleft_frame, text="Total Tax Amount:").grid(row = 4, column = 0, padx = 10, pady = 10)
        ttk.Label(self.bottom_right_subleft_frame, text="Total After Tax Amount:").grid(row = 5, column = 0, padx = 10, pady = 10)
        ttk.Label(self.bottom_right_subleft_frame, text="GST on Reverse Charges:").grid(row = 6, column = 0, padx = 10, pady = 10)

        ''' ENTRY WIDGETS '''

        ''' Purchase / Sale option '''
        self.typeVar = tk.IntVar(self.window)

        self.purchase_radio_button = ttk.Radiobutton(
            self.bottom_left_subleft_frame, text="Purchase", variable=self.typeVar, value=0)
        self.purchase_radio_button.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.sale_radio_button = ttk.Radiobutton(
            self.bottom_left_subright_frame, text="Sale", variable=self.typeVar, value=1)
        self.sale_radio_button.grid(row = 0, column = 1, padx = 10, pady = 10)


        self.entry_invoice_no = ttk.Entry(self.top_left_subright_frame, text=self.invoice_number_default)
        self.entry_invoice_no.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.entry_invoice_date = ttk.Entry(self.top_left_subright_frame, textvariable=self.dating)  # date picker
        self.entry_invoice_date.grid(row = 1, column = 1, padx = 10, pady = 10)
        
        self.reverse_charge_var = tk.BooleanVar(self.window, value = False)

        self.reverse_frame = ttk.Frame(self.top_left_subright_frame)
        self.reverse_frame.grid(row = 2, column = 1, padx = 10, pady = 10)

        self.reverse_true_radio_button = ttk.Radiobutton(
            self.reverse_frame, text="Yes", variable=self.reverse_charge_var, value=True)
        self.reverse_true_radio_button.pack(side = tk.LEFT, expand = True)

        self.reverse_false_radio_button = ttk.Radiobutton(
            self.reverse_frame, text="No", variable=self.reverse_charge_var, value=False)
        self.reverse_false_radio_button.pack(side = tk.RIGHT, expand = True)

        
        self.entry_state = ttk.Entry(self.top_left_subright_frame)
        self.entry_state.grid(row = 3, column = 1, padx = 10, pady = 10)
        self.entry_code = ttk.Entry(self.top_left_subright_frame)
        self.entry_code.grid(row = 4, column = 1, padx = 10, pady = 10)

        self.entry_party_name = ttk.Entry(self.top_right_subright_frame, width=32)
        self.entry_party_name.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.entry_party_address = tk.Text(self.top_right_subright_frame, height=2, width=24)  # Address
        self.entry_party_address.grid(row = 1, column = 1, padx = 10, pady = 10)
        self.entry_party_gstin = ttk.Entry(self.top_right_subright_frame, width=32)
        self.entry_party_gstin.grid(row = 2, column = 1, padx = 10, pady = 10)
        self.entry_party_state = ttk.Entry(self.top_right_subright_frame)
        self.entry_party_state.grid(row = 3, column = 1, padx = 10, pady = 10)
        self.entry_party_code = ttk.Entry(self.top_right_subright_frame)
        self.entry_party_code.grid(row = 4, column = 1, padx = 10, pady = 10)

        self.entry_rs_in_words = ttk.Entry(self.bottom_left_subright_frame)
        self.entry_rs_in_words.grid(row = 1, column = 1, padx = 10, pady = 10)
        self.entry_bank_name = ttk.Entry(self.bottom_left_subright_frame)
        self.entry_bank_name.grid(row = 2, column = 1, padx = 10, pady = 10)
        self.entry_ac_no = ttk.Entry(self.bottom_left_subright_frame)
        self.entry_ac_no.grid(row = 3, column = 1, padx = 10, pady = 10)
        self.entry_ifc_code = ttk.Entry(self.bottom_left_subright_frame)
        self.entry_ifc_code.grid(row = 5, column = 1, padx = 10, pady = 10)

        self.entry_total_before_tax = ttk.Entry(self.bottom_right_subright_frame)
        self.entry_total_before_tax.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.entry_igst = ttk.Entry(self.bottom_right_subright_frame)
        self.entry_igst.grid(row = 1, column = 1, padx = 10, pady = 10)
        self.entry_cgst = ttk.Entry(self.bottom_right_subright_frame)
        self.entry_cgst.grid(row = 2, column = 1, padx = 10, pady = 10)
        self.entry_sgst = ttk.Entry(self.bottom_right_subright_frame)
        self.entry_sgst.grid(row = 3, column = 1, padx = 10, pady = 10)
        self.entry_total_tax_amt = ttk.Entry(self.bottom_right_subright_frame)
        self.entry_total_tax_amt.grid(row = 4, column = 1, padx = 10, pady = 10)
        self.entry_total_after_tax_amt = ttk.Entry(self.bottom_right_subright_frame)
        self.entry_total_after_tax_amt.grid(row = 5, column = 1, padx = 10, pady = 10)
        self.entry_gst_reverse_charge = ttk.Entry(self.bottom_right_subright_frame)
        self.entry_gst_reverse_charge.grid(row = 6, column = 1, padx = 10, pady = 10)

        self.entry_invoice_date.bind("<1>", self.calOpen)

        '''Generating goods details'''
        self.goods_table = Table(self.window)

        ''' AutoFill Party '''
        self.autofill_var = tk.StringVar(self.window)
        
        self.autofill_entity_options = [i[0] for i in models.get_all_entity_names()]
        self.options_autofill = ttk.OptionMenu(
            self.header_frame, self.autofill_var, "None", *self.autofill_entity_options
        )
        self.options_autofill.grid(row = 0, column = 3, padx = 10, pady = 10)

        self.btn_autofill_party = ttk.Button(
            self.header_frame, text='AutoFill Entity',
            width=30, command=self.autofill_entity_fields
        )
        self.btn_autofill_party.grid(row = 0, column = 4, padx = 10, pady = 10)


        ''' Calculate Button '''
        self.btn_deets_calculate = ttk.Button(
            self.footer_frame, text='Calculate', command=self.onCalculate,
            width=30
        )
        self.btn_deets_calculate.grid(row = 0, column = 0, padx = 10, pady = 10)

        ''' Submit Button'''

        self.btn_invoice_submit = ttk.Button(
            self.footer_frame, text="Submit", command=self.onSubmit,
            width=30
        )
        self.btn_invoice_submit.grid(row = 0, column = 1, padx = 10, pady = 10)

        self.btn_invoice_print = ttk.Button(
            self.footer_frame, text='Print', command=self.onPrint,
            width=30
        )
        self.btn_invoice_print.grid(row=0, column=2, padx=10, pady=10)

        ''' Window Mainloop '''
        self.window.mainloop()

    def back_to_home_page(self):
        self.window.destroy()

    def calOpen(self, event):
        CalWindow(self.dating)

    def insertInvoice(self):
        print(datetime.strptime(
            self.entry_invoice_date.get(), '%d/%m/%Y'))
        resp = createInvoice(
            invoice_date=datetime.strptime(
                self.entry_invoice_date.get(), '%d/%m/%Y'),
            invoice_no=self.entry_invoice_no.get(),
            name=self.entry_party_name.get(),
            address=self.entry_party_address.get('1.0', 'end-1c'),
            gst=self.entry_party_gstin.get(),
            state=self.entry_party_state.get(),
            state_code=self.entry_party_code.get(),
            total=self.entry_total_tax_amt.get(),
            total_cgst=self.entry_cgst.get(),
            total_sgst=self.entry_sgst.get(),
            purchase=self.typeVar.get(),
            reverse_charges=self.reverse_charge_var.get()
        )
        print(resp)
        return resp

    def insertDetails(self, inv_id):
        deets = self.goods_table.getGoodsDetails()
        errors = 0
        for deet in deets:
            x = createDetails(
                deet_no = deet["deet_no"] ,
                invoice_id = inv_id,
                name = deet["name"],
                batch = deet['batch'],
                hsn = deet["hsn"],
                qty = deet["qty"],
                rate = deet["rate"],
                mrp = deet["mrp"],
                total = deet["total"],
                discount = deet["discount"],
                taxable_amt = deet["taxable_amt"]
            )
            if not x:
                errors += 1
        print("Errors:", errors)
        return

    def performCaluclations(self):
        base_val = 0.0
        try:
            dets = self.goods_table.getGoodsDetails()
            j = 0
            total = 0
            for i in dets:
                ''' check for null '''
                for field in i:
                    if i[field] == "" or not i[field]:
                        continue
                
                ''' continue '''
                if i['deet_no'] != '':
                    i['total'] = 0
                    #print(i['qty'], i["rate"])
                    i['total'] = int(i['qty']) * int(i['rate'])
                    i['taxable_amt'] = int(i['total'] - int(i['discount']))
                    total = total + i['taxable_amt']
                    print(self.goods_table.entries[j])
                    print(self.goods_table.entries[j]['total'].set(i['total']))
                    self.goods_table.entries[j]['taxable_amt'].set(
                        int(i['total']) - int(i['discount']))
                    j = j + 1
            # if self.entry_total_before_tax.get()) > 0:
            #     self.change_bottom_right()
            
            self.entry_rs_in_words.delete(0, END)
            self.entry_total_before_tax.delete(0, END)
            self.entry_cgst.delete(0, END)
            self.entry_igst.delete(0, END)
            self.entry_sgst.delete(0, END)
            self.entry_total_tax_amt.delete(0, END)
            self.entry_total_after_tax_amt.delete(0, END)
            
            self.entry_total_before_tax.insert(0, round(total, 2))
            self.entry_cgst.insert(0, round(total * 0.06, 2))
            self.entry_igst.insert(0, round(total * 0.06, 2))
            self.entry_sgst.insert(0, round(total * 0.06, 2))
            self.entry_total_tax_amt.insert(0, round(total * 0.12, 2))
            self.entry_total_after_tax_amt.insert(0, round(total + total * 0.12, 2))
            self.entry_rs_in_words.insert(0, num2words(self.entry_total_after_tax_amt.get()).title())
        except Exception as e:
            print(e)
            self.sendAlert("Error while calculating!")
    

    def onConfirm(self):
        print('Confirmed')
        inv_id = self.insertInvoice()
        print("Invoice id generated:", inv_id)
        if inv_id:
            x = self.insertDetails(inv_id)
            print(x)
            if x:
                messagebox.showinfo(title='Invoice Status',
                                    message='Invoice and details have been successfully recorded')
                
                self.back_to_home_page()

    def onCalculate(self):
        global CAL_CLICKED
        CAL_CLICKED += 1
        self.performCaluclations()
        if not self.validateData():
            self.sendAlert("Invalid Data! Should not contain any empty fields")

    
    def onSubmit(self):
        if CAL_CLICKED >= 1:
            if not self.validateData():
                self.sendAlert("Invalid Data! Should not contain any empty fields")
                return False
            self.onConfirm()

        else:
            messagebox.showerror(
                title='Attention', message='Please click calculate button before submission')

        
    def onPrint(self):
        good_deets = self.goods_table.getGoodsDetails()
        filename_with_Abspath = filedialog.asksaveasfilename(defaultextension='.pdf', title='Save Invoice') 

        compete_invoice_details = {
            'invoice_details': {
                'invoice_date'    : datetime.strptime(self.entry_invoice_date.get(), '%d/%m/%Y'),
                'invoice_no'      : self.entry_invoice_no.get(),
                'name'            : self.entry_party_name.get(),
                'address'         : self.entry_party_address.get('1.0', 'end-1c'),
                'gst'             : self.entry_party_gstin.get(),
                'state'           : self.entry_party_state.get(),
                'state_code'      : self.entry_party_code.get(),
                'total'           : self.entry_total_tax_amt.get(),
                'total_cgst'      : self.entry_cgst.get(),
                'total_sgst'      : self.entry_sgst.get(),
                'purchase'        : self.typeVar.get(),
                'reverse_charges' : self.reverse_charge_var.get(),
                'rupess_in_words' : self.entry_rs_in_words.get(),
                'bank_name'       : self.entry_bank_name.get(),
                'bank_account'    : self.entry_ac_no.get(),
                'ifsc_code'       : self.entry_ifc_code.get()
            },

            'goods_details'       : good_deets,
            'filepath_with_name'  : filename_with_Abspath
        }

        print(compete_invoice_details)
        printing = create_invoice_pdf(compete_invoice_details['invoice_details'], compete_invoice_details['goods_details'])


    def validateData(self):
        goods_details = self.goods_table.getGoodsDetails()
        if goods_details == []:
            return False
        return True
    

    def sendAlert(self, message):
        messagebox.showerror(title='Error', message=message)


    def autofill_entity_fields(self):
        res = models.get_entity_by_name(self.autofill_var.get())
        if res == None:
            messagebox.showerror(title='Error', message='No saved items were found.')
            return
        x = {field: res.__dict__[field] for field in res.__dict__}
        #print(x)

        try:
            self.entry_party_name.delete(0, tk.END)
            self.entry_party_name.insert(0, x["name"])
            
            self.entry_ifc_code.delete(0, tk.END)
            self.entry_ifc_code.insert(0, x["ifc_code"])

            self.entry_bank_name.delete(0, tk.END)
            self.entry_bank_name.insert(0, x["bank_name"])

            self.entry_party_state.delete(0, tk.END)
            self.entry_party_state.insert(0, x["state"])

            self.entry_party_address.delete("1.0", tk.END)
            self.entry_party_address.insert("1.0", x["address"])

            self.entry_ac_no.delete(0, tk.END)
            self.entry_ac_no.insert(0, x["a_c_no"])
            
            self.entry_party_code.delete(0, tk.END)
            self.entry_party_code.insert(0, x["state_code"])
            
            self.entry_party_gstin.delete(0, tk.END)
            self.entry_party_gstin.insert(0, x["gstin_uid"])
        except Exception as e:
            print(e)