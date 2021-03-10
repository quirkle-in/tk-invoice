from pdf_generation.create_invoice_pdf import create_invoice_pdf
from gui.components import goods_table
from gui.components import datepick
from ttkthemes import ThemedStyle
from models import createInvoice
from num2words import num2words
from tkinter import filedialog
from tkinter import messagebox
from datetime import datetime
from tkinter import ttk
from tkinter import END
import tkinter as tk
import models


CAL_CLICKED = 0

class InvoiceForm:
    def __init__(self):

        self.window = tk.Tk()
        self.window.configure(background="#f3f3f3")
        self.window.title("Create Invoice")
        self.window.geometry("1200x700")
        self.window.resizable(True, True)

        style = ThemedStyle(self.window)
        style.set_theme("vista")


        ''' TK VARIABLES '''
        self.reverse_charge_var = tk.BooleanVar(self.window, value = False)
        self.typeVar = tk.IntVar(self.window)
        self.invoice_number_default = tk.IntVar(self.window)
        self.autofill_var = tk.StringVar(self.window)
        ''' DATE PICKER STRING VAR '''
        self.dating = tk.StringVar(self.window)
        self.dating.set(datetime.now().strftime("%d/%m/%Y"))


        ''' GET DATA '''
        try:
            x = models.get_last_invoice()
            if not x: return
            else: self.invoice_number_default.set(x)
        except Exception as e:
            print(e)
            self.window.destroy()
            return

        ''' INVOICE DICT '''
        self.invoice_data = {}


        self.header_frame = ttk.Frame(self.window)
        self.header_frame.pack(expand = True, padx = 10, pady = 5)
        # -
        self.top_frame = ttk.Frame(self.window)
        self.top_frame.pack(side = tk.TOP, expand=True, anchor="n")

        # - -
        self.top_left_frame = ttk.Frame(self.top_frame, borderwidth=2, relief="groove")
        self.top_left_frame.pack(side = tk.LEFT, anchor="n")
        
        # - -
        self.top_right_frame = ttk.Frame(self.top_frame, borderwidth=2, relief="groove")
        self.top_right_frame.pack(side = tk.RIGHT, anchor="n")
    
        ''' FOOTER '''
    
        self.footer_frame = ttk.Frame(self.window, borderwidth=2, relief="groove")
        self.footer_frame.pack(side = tk.BOTTOM)

        ''' BOTTOM '''
        # -
        self.bottom_frame = ttk.Frame(self.window)
        self.bottom_frame.pack(side = tk.BOTTOM, expand = True, anchor="n")

        # - -
        self.bottom_left_frame = ttk.Frame(self.bottom_frame, borderwidth=2, relief="groove")
        self.bottom_left_frame.pack(side = tk.LEFT, anchor="n")
        
        # - -
        self.bottom_right_frame = ttk.Frame(self.bottom_frame, borderwidth=2, relief="groove")
        self.bottom_right_frame.pack(side = tk.RIGHT, anchor="n")

        ''' WIDGETS '''

        ''' HEADER '''

        self.back_to_home = ttk.Button(self.header_frame, text="Back", command=self.back_to_home_page)
        self.back_to_home.grid(row = 0, column = 0, padx = 90, pady = 5)

        ttk.Label(self.header_frame, text="TAX INVOICE", font=("Arial", 16, "bold")).grid(row = 0, column = 1, padx = 200, pady = 5)

        ''' AutoFill Party '''
        self.autofill_entity_options = [i[0] for i in models.get_all_entity_names()]
        self.options_autofill = ttk.OptionMenu(self.header_frame, self.autofill_var, "None", *self.autofill_entity_options)
        self.options_autofill.grid(row = 0, column = 3, padx = 10, pady = 5)
        self.btn_autofill_party = ttk.Button(self.header_frame, text='AutoFill Entity',width=20, command=self.autofill_entity_fields)
        self.btn_autofill_party.grid(row = 0, column = 4)

        ''' TOP '''
        
        x = ttk.Frame(self.top_left_frame)
        ttk.Label(x, text="Invoice Number:").pack(side = tk.LEFT, expand = True, padx = 10, pady = 5)
        self.entry_invoice_no = ttk.Entry(x, text=self.invoice_number_default)
        self.entry_invoice_no.pack(side = tk.RIGHT, expand = True, padx = 10, pady = 5)
        x.pack()
        
        x = ttk.Frame(self.top_left_frame)
        ttk.Label(x, text="Invoice Date:").pack(side = tk.LEFT, expand = True, padx = 10, pady = 5)
        self.entry_invoice_date = ttk.Entry(x, textvariable=self.dating)  # date picker
        self.entry_invoice_date.pack(side = tk.RIGHT, expand = True, padx = 10, pady = 5)
        x.pack()
        
        
        x = ttk.Frame(self.top_left_frame)
        ttk.Label(x, text="Reverse Charges:").pack(side = tk.LEFT, expand = True, padx = 10, pady = 5)
        self.reverse_frame = ttk.Frame(x)
        self.reverse_frame.pack(side = tk.RIGHT, expand = True, padx = 10, pady = 5)
        self.reverse_true_radio_button = ttk.Radiobutton(self.reverse_frame, text="Yes", variable=self.reverse_charge_var, value=True)
        self.reverse_true_radio_button.pack(side = tk.LEFT, expand = True)
        self.reverse_false_radio_button = ttk.Radiobutton(self.reverse_frame, text="No", variable=self.reverse_charge_var, value=False)
        self.reverse_false_radio_button.pack(side = tk.RIGHT, expand = True)
        x.pack()
        
        x = ttk.Frame(self.top_left_frame)
        ttk.Label(x, text="State:").pack(side = tk.LEFT, expand = True, padx = 10, pady = 5)
        self.entry_state = ttk.Entry(x)
        self.entry_state.pack(side = tk.LEFT, expand = True, padx = 10, pady = 5)
        self.entry_state.insert(0, 'Maharashtra')
        
        self.entry_code = ttk.Entry(x)
        self.entry_code.pack(side = tk.RIGHT, expand = True, padx = 10, pady = 5)
        ttk.Label(x, text="Code:").pack(side = tk.RIGHT, expand = True, padx = 10, pady = 5)
        x.pack()

        x = ttk.Frame(self.top_right_frame)
        ttk.Label(x, text="BILL TO PARTY").pack(expand = True, padx = 10, pady = 5)
        x.pack()
        
        x = ttk.Frame(self.top_right_frame)
        ttk.Label(x, text="Name:").pack(side = tk.LEFT, expand = True, padx = 10, pady = 5)
        self.entry_party_name = ttk.Entry(x, width=32)
        self.entry_party_name.pack(side = tk.RIGHT, expand = True, padx = 10, pady = 5)
        x.pack()
        
        x = ttk.Frame(self.top_right_frame)
        ttk.Label(x, text="Address:").pack(side = tk.LEFT, expand = True, padx = 10, pady = 5)
        self.entry_party_address = tk.Text(x, height=2, width=24)  # Address
        self.entry_party_address.pack(side = tk.RIGHT, expand = True, padx = 10, pady = 5)
        x.pack()
        
        x = ttk.Frame(self.top_right_frame)
        ttk.Label(x, text="GSTIN Unique ID:").pack(side = tk.LEFT, expand = True, padx = 10, pady = 5)
        self.entry_party_gstin = ttk.Entry(x, width=32)
        self.entry_party_gstin.pack(side = tk.RIGHT, expand = True, padx = 10, pady = 5)
        x.pack()
        
        x = ttk.Frame(self.top_right_frame)
        ttk.Label(x, text="State:").pack(side = tk.LEFT, expand = True, padx = 10, pady = 5)
        self.entry_party_state = ttk.Entry(x)
        self.entry_party_state.pack(side = tk.LEFT, expand = True, padx = 10, pady = 5)

        self.entry_party_code = ttk.Entry(x)
        self.entry_party_code.pack(side = tk.RIGHT, expand = True, padx = 10, pady = 5)
        ttk.Label(x, text="State Code:").pack(side = tk.RIGHT, expand = True, padx = 10, pady = 5)
        x.pack()

        ''' GOODS FORM / LISTBOX '''

        ttk.Label(self.window, text="GOODS", font=("Arial", 11, "bold")).pack(expand = True)
        self.goods_table = goods_table.Table(self.window)

        ''' Purchase / Sale option '''
        x = ttk.Frame(self.bottom_left_frame)
        self.purchase_radio_button = ttk.Radiobutton(x, text="Purchase", variable=self.typeVar, value=0)
        self.purchase_radio_button.pack(side = tk.LEFT, expand = True, padx = 10, pady = 5)

        self.sale_radio_button = ttk.Radiobutton(x, text="Sale", variable=self.typeVar, value=1)
        self.sale_radio_button.pack(side = tk.RIGHT, expand = True, padx = 10, pady = 5)
        x.pack()

        x = ttk.Frame(self.bottom_left_frame)
        ttk.Label(x, text="Rs. in Words:").pack(side = tk.LEFT, expand = True, padx = 10, pady = 5)
        self.entry_rs_in_words = ttk.Entry(x)
        self.entry_rs_in_words.pack(side = tk.RIGHT, expand = True, padx = 10, pady = 5)
        x.pack()

        #ttk.Label(self.bottom_left_subleft_frame, text="AYURVEDIC PROP MEDICINE").grid(row = 2, column = 0, padx = 10, pady = 5)
        
        x = ttk.Frame(self.bottom_left_frame)
        ttk.Label(x, text="Bank Name:").pack(side = tk.LEFT, expand = True, padx = 10, pady = 5)
        self.entry_bank_name = ttk.Entry(x)
        self.entry_bank_name.pack(side = tk.RIGHT, expand = True, padx = 10, pady = 5)
        x.pack()

        x = ttk.Frame(self.bottom_left_frame)
        ttk.Label(x, text="A/c No.:").pack(side = tk.LEFT, expand = True, padx = 10, pady = 5)
        self.entry_ac_no = ttk.Entry(x)
        self.entry_ac_no.pack(side = tk.RIGHT, expand = True, padx = 10, pady = 5)
        x.pack()

        x = ttk.Frame(self.bottom_left_frame)
        ttk.Label(x, text="IFS Code:").pack(side = tk.LEFT, expand = True, padx = 10, pady = 5)
        self.entry_ifc_code = ttk.Entry(x)
        self.entry_ifc_code.pack(side = tk.RIGHT, expand = True, padx = 10, pady = 5)
        x.pack()
        
        x = ttk.Frame(self.bottom_right_frame)
        ttk.Label(x, text="Total Before Tax:").pack(side = tk.LEFT, expand = True, padx = 10, pady = 5)
        self.entry_total_before_tax = ttk.Entry(x)
        self.entry_total_before_tax.pack(side = tk.RIGHT, expand = True, padx = 10, pady = 5)
        x.pack()
        
        x = ttk.Frame(self.bottom_right_frame)
        ttk.Label(x, text="IGST:").pack(side = tk.LEFT, expand = True, padx = 10, pady = 5)
        self.entry_igst = ttk.Entry(x)
        self.entry_igst.pack(side = tk.RIGHT, expand = True, padx = 10, pady = 5)
        x.pack()
        
        x = ttk.Frame(self.bottom_right_frame)
        ttk.Label(x, text="CGST@ 6%:").pack(side = tk.LEFT, expand = True, padx = 10, pady = 5)
        self.entry_cgst = ttk.Entry(x)
        self.entry_cgst.pack(side = tk.RIGHT, expand = True, padx = 10, pady = 5)
        x.pack()
        
        x = ttk.Frame(self.bottom_right_frame)
        ttk.Label(x, text="SGST@ 6%:").pack(side = tk.LEFT, expand = True, padx = 10, pady = 5)
        self.entry_sgst = ttk.Entry(x)
        self.entry_sgst.pack(side = tk.RIGHT, expand = True, padx = 10, pady = 5)
        x.pack()
        
        x = ttk.Frame(self.bottom_right_frame)
        ttk.Label(x, text="Total Tax Amount:").pack(side = tk.LEFT, expand = True, padx = 10, pady = 5)
        self.entry_total_tax_amt = ttk.Entry(x)
        self.entry_total_tax_amt.pack(side = tk.RIGHT, expand = True, padx = 10, pady = 5)
        x.pack()
        
        x = ttk.Frame(self.bottom_right_frame)
        ttk.Label(x, text="Total After Tax Amount:").pack(side = tk.LEFT, expand = True, padx = 10, pady = 5)
        self.entry_total_after_tax_amt = ttk.Entry(x)
        self.entry_total_after_tax_amt.pack(side = tk.RIGHT, expand = True, padx = 10, pady = 5)
        x.pack()
        
        x = ttk.Frame(self.bottom_right_frame)
        ttk.Label(x, text="GST on Reverse Charges:").pack(side = tk.LEFT, expand = True, padx = 10, pady = 5)
        self.entry_gst_reverse_charge = ttk.Entry(x)
        self.entry_gst_reverse_charge.pack(side = tk.RIGHT, expand = True, padx = 10, pady = 5)
        x.pack()

        self.entry_invoice_date.bind("<1>", self.calOpen)

        ''' Calculate Button '''
        self.btn_deets_calculate = ttk.Button(self.footer_frame, text='Calculate', command=self.onCalculate,width=30)
        self.btn_deets_calculate.grid(row = 0, column = 0, padx = 10, pady = 5)

        ''' Submit Button'''
        self.btn_invoice_submit = ttk.Button(self.footer_frame, text="Submit", command=self.onSubmit,width=30)
        self.btn_invoice_submit.grid(row = 0, column = 1, padx = 10, pady = 5)

        self.btn_invoice_print = ttk.Button(self.footer_frame, text='Print', command=self.onPrint,width=30)
        self.btn_invoice_print.grid(row=0, column=2, padx=10, pady=10)

        ''' Window Mainloop '''
        self.window.mainloop()


    def back_to_home_page(self):
        self.window.destroy()


    def calOpen(self, event):
        datepick.CalWindow(self.dating)


    def insertInvoice(self):
        resp = createInvoice(self.invoice_data)
        print("Create invoice response:", resp)
        return resp

    def insertDetails(self, inv_id):
        deets = self.goods_table.getGoodsDetails()
        errors = 0
        for deet in deets:
            x = models.createDetails(
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
        return True

    def performCaluclations(self):
        try:
            dets = self.goods_table.getGoodsDetails()
            j = 0; total = 0
            for i in dets:

                ''' check for null '''
                for field in i:
                    if i[field] == "" or not i[field]:
                        continue
                
                ''' continue '''
                if i['deet_no'] != '':
                    i['total'] = int(i['qty']) * int(i['rate'])
                    i['taxable_amt'] = int(i['total'] - int(i['discount']))
                    total = total + i['taxable_amt']

                    print(self.goods_table.entries[j])
                    print(self.goods_table.entries[j]['total'].set(i['total']))

                    self.goods_table.entries[j]['taxable_amt'].set(int(i['total']) - int(i['discount']))
                    j = j + 1

            ''' clear fields before inserting '''
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
        print('Confirming...')

        ''' collect data '''
        self.collect_field_data()

        ''' insert '''
        inv_id = self.insertInvoice()
        if inv_id:
            print("Invoice created.")
            x = self.insertDetails(inv_id)
            if x:
                print("Details recorded.")
                messagebox.showinfo(title='Invoice Status', message='Invoice and details have been successfully recorded')
                return True

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
            res = self.onConfirm()
            if not res:
                self.sendAlert("Error while creating.")

        else:
            messagebox.showerror(title='Attention', message='Please click calculate button before submission')
    
    def collect_field_data(self):
        self.invoice_data = {
            "invoice_date" :        datetime.strptime(self.entry_invoice_date.get(), '%d/%m/%Y'),
            "invoice_no" :          self.entry_invoice_no.get(),
            "name" :                self.entry_party_name.get(),
            "address" :             self.entry_party_address.get('1.0', 'end-1c'),
            "gst" :                 self.entry_party_gstin.get(),
            "state" :               self.entry_party_state.get(),
            "state_code" :          self.entry_party_code.get(),
            "total" :               self.entry_total_tax_amt.get(),
            "total_cgst" :          self.entry_cgst.get(),
            "total_sgst" :          self.entry_sgst.get(),
            "purchase" :            self.typeVar.get(),
            "rupees_in_words" :     self.entry_rs_in_words.get(),
            "reverse_charges" :     self.reverse_charge_var.get(),
            "bank_name" :           self.entry_bank_name.get(),
            "gst_reverse_charge" :  self.entry_gst_reverse_charge.get(),
            "total_before_tax" :    self.entry_total_before_tax.get(),
            "total_after_tax" :     self.entry_total_after_tax_amt.get(),
            "total_igst" :          self.entry_igst.get(),
            "total_tax_amt" :       self.entry_total_tax_amt.get()
        }

    def collect_goods_details_data(self):
        pass
        
    def onPrint(self):
        good_deets = self.goods_table.getGoodsDetails()
        filename_with_Abspath = filedialog.asksaveasfilename(defaultextension='.pdf', title='Save Invoice') 

        complete_invoice_details = {
            'invoice_details': {
                'invoice_date'    : datetime.strptime(self.entry_invoice_date.get(), '%d/%m/%Y'),
                'invoice_no'      : self.entry_invoice_no.get(),
                'name'            : self.entry_party_name.get(),
                'address'         : self.entry_party_address.get('1.0', 'end-1c'),
                'gst'             : self.entry_party_gstin.get(),
                'state'           : self.entry_party_state.get(),
                'state_code'      : self.entry_party_code.get(),
                'total'           : self.entry_total_tax_amt.get(),
                'total_before_tax': self.entry_total_before_tax.get(),
                'total_igst'      : self.entry_igst.get(),
                'total_tax_amt'   : self.entry_total_tax_amt.get(),
                'total_after_tax' : self.entry_total_after_tax_amt.get(),
                'gst_reverse_charge' : self.entry_gst_reverse_charge.get(),
                'total_cgst'      : self.entry_cgst.get(),
                'total_sgst'      : self.entry_sgst.get(),
                'purchase'        : self.typeVar.get(),
                'reverse_charges' : self.reverse_charge_var.get(),
                'rupees_in_words' : self.entry_rs_in_words.get(),
                'bank_name'       : self.entry_bank_name.get(),
                'account_no'    : self.entry_ac_no.get(),
                'ifsc_code'       : self.entry_ifc_code.get(),
            },

            'goods_details'       : good_deets,
            'filepath_with_name'  : filename_with_Abspath
        }

        print(complete_invoice_details)
        printing = create_invoice_pdf(complete_invoice_details['invoice_details'], 
                                    complete_invoice_details['goods_details'],
                                    complete_invoice_details['filepath_with_name']
                                    )


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