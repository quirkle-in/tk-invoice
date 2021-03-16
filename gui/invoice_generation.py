from pdf_generation.create_invoice_pdf import create_invoice_pdf
from tkinter.scrolledtext import ScrolledText
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
import json


CAL_CLICKED = 0


class InvoiceForm:
    def __init__(self, SETTINGS, main_window):
        self.SETTINGS = SETTINGS
        self.main_window = main_window

        self.window = tk.Tk()
        self.window.title(f'{self.SETTINGS["pdf_title"]} | Create Invoice')
        self.window.geometry("1200x800")
        self.window.resizable(True, True)

        style = ThemedStyle(self.window)
        style.set_theme(self.SETTINGS["theme"])

        self.window.iconbitmap('favicon.ico')

        ''' TK VARIABLES '''
        self.reverse_charge_var = tk.BooleanVar(self.window, value=False)
        self.typeVar = tk.BooleanVar(self.window, value=True)
        self.invoice_number_default = tk.IntVar(self.window)
        self.autofill_var = tk.StringVar(self.window)
        ''' DATE PICKER STRING VAR '''
        self.dating = tk.StringVar(self.window)
        self.dating.set(datetime.now().strftime("%d/%m/%Y"))

        ''' GET DATA '''
        self.set_invoice_id()

        ''' INVOICE DATA '''
        self.invoice_data = {}
        self.goods_details = []

        self.header_frame = ttk.Frame(self.window)
        self.header_frame.pack(expand=True, padx=10, pady=5)
        # -
        self.top_frame = ttk.Frame(self.window)
        self.top_frame.pack(side=tk.TOP, expand=True, anchor="n", padx=10)

        # - -
        self.top_left_frame = ttk.Frame(
            self.top_frame, borderwidth=2, relief="groove")
        self.top_left_frame.pack(side=tk.LEFT, anchor="n", padx=10)

        # - -
        self.top_right_frame = ttk.Frame(
            self.top_frame, borderwidth=2, relief="groove")
        self.top_right_frame.pack(side=tk.RIGHT, anchor="n", padx=10)

        ''' BOTTOM '''
        # -
        self.bottom_frame = ttk.Frame(self.window)
        self.bottom_frame.pack(
            side=tk.BOTTOM, expand=True, anchor="n", padx=10)

        # - -
        self.bottom_left_frame = ttk.Frame(
            self.bottom_frame, borderwidth=2, relief="groove")
        self.bottom_left_frame.pack(side=tk.LEFT, anchor="n", padx=10)

        # - -
        self.bottom_right_frame = ttk.Frame(
            self.bottom_frame, borderwidth=2, relief="groove")
        self.bottom_right_frame.pack(side=tk.LEFT, anchor="n", padx=10)

        ''' FOOTER '''
        self.footer_frame = ttk.Frame(
            self.bottom_frame, borderwidth=2, relief="groove")
        self.footer_frame.pack(side=tk.RIGHT, padx=10)

        ''' WIDGETS '''

        ''' HEADER '''

        self.back_to_home = ttk.Button(
            self.header_frame, text="Back", command=self.back_to_home_page)
        self.back_to_home.grid(row=0, column=0, padx=90, pady=5)

        ttk.Label(self.header_frame, text="CREATE A TAX INVOICE", font=(
            "Arial", 16, "bold")).grid(row=0, column=1, padx=200, pady=5)

        ''' AutoFill Party '''
        self.autofill_entity_options = [i[0]
                                        for i in models.get_all_entity_names()]
        self.options_autofill = ttk.OptionMenu(
            self.header_frame, self.autofill_var, "None", *self.autofill_entity_options)
        self.options_autofill.grid(row=0, column=3, padx=10, pady=5)
        self.btn_autofill_party = ttk.Button(
            self.header_frame, text='AutoFill Entity', width=20, command=self.autofill_entity_fields)
        self.btn_autofill_party.grid(row=0, column=4)

        ''' TOP '''

        x = ttk.Frame(self.top_left_frame)
        ttk.Label(x, text="Invoice Number:").pack(
            side=tk.LEFT, expand=True, padx=10, pady=5)
        self.entry_invoice_no = ttk.Entry(x, text=self.invoice_number_default)
        self.entry_invoice_no.pack(side=tk.RIGHT, expand=True, padx=10, pady=5)
        x.pack()

        x = ttk.Frame(self.top_left_frame)
        ttk.Label(x, text="Invoice Date:").pack(
            side=tk.LEFT, expand=True, padx=18, pady=5)
        self.entry_invoice_date = ttk.Entry(
            x, textvariable=self.dating)  # date picker
        self.entry_invoice_date.pack(
            side=tk.RIGHT, expand=True, padx=10, pady=5)
        x.pack()

        x = ttk.Frame(self.top_left_frame)
        ttk.Label(x, text="Reverse Charges:").pack(
            side=tk.LEFT, expand=True, padx=10, pady=5)
        self.reverse_frame = ttk.Frame(x)
        self.reverse_frame.pack(side=tk.RIGHT, expand=True, padx=10, pady=5)
        self.reverse_true_radio_button = ttk.Radiobutton(
            self.reverse_frame, text="Yes", variable=self.reverse_charge_var, value=True)
        self.reverse_true_radio_button.pack(side=tk.LEFT, expand=True, padx=10)
        self.reverse_false_radio_button = ttk.Radiobutton(
            self.reverse_frame, text="No", variable=self.reverse_charge_var, value=False)
        self.reverse_false_radio_button.pack(
            side=tk.RIGHT, expand=True, padx=10)
        x.pack()

        x = ttk.Frame(self.top_left_frame)
        ttk.Label(x, text="State:").pack(
            side=tk.LEFT, expand=True, padx=10, pady=5)
        self.entry_state = ttk.Entry(x)
        self.entry_state.insert(0, self.SETTINGS["state"])
        self.entry_state.pack(side=tk.LEFT, expand=True, padx=10, pady=5)

        self.entry_code = ttk.Entry(x)
        self.entry_code.pack(side=tk.RIGHT, expand=True, padx=10, pady=5)
        ttk.Label(x, text="Code:").pack(
            side=tk.RIGHT, expand=True, padx=10, pady=5)
        x.pack()

        x = ttk.Frame(self.top_right_frame)
        ttk.Label(x, text="BILL TO PARTY").pack(expand=True, padx=10, pady=5)
        x.pack()

        x = ttk.Frame(self.top_right_frame)
        ttk.Label(x, text="Name:").pack(
            side=tk.LEFT, expand=True, padx=10, pady=5)
        self.entry_party_name = ttk.Entry(x, width=48)
        self.entry_party_name.pack(side=tk.RIGHT, expand=True, padx=10, pady=5)
        x.pack()

        x = ttk.Frame(self.top_right_frame)
        ttk.Label(x, text="Address:").pack(
            side=tk.LEFT, expand=True, padx=10, pady=5)
        self.entry_party_address = ScrolledText(
            x, height=2, width=48, wrap=tk.WORD)  # Address
        self.entry_party_address.pack(
            side=tk.RIGHT, expand=True, padx=10, pady=5)
        x.pack()

        x = ttk.Frame(self.top_right_frame)
        ttk.Label(x, text="GSTIN Unique ID:").pack(
            side=tk.LEFT, expand=True, padx=10, pady=5)
        self.entry_party_gstin = ttk.Entry(x, width=42)
        self.entry_party_gstin.pack(
            side=tk.RIGHT, expand=True, padx=10, pady=5)
        x.pack()

        x = ttk.Frame(self.top_right_frame)
        ttk.Label(x, text="State:").pack(
            side=tk.LEFT, expand=True, padx=10, pady=5)
        self.entry_party_state = ttk.Entry(x)
        self.entry_party_state.pack(side=tk.LEFT, expand=True, padx=10, pady=5)

        self.entry_party_code = ttk.Entry(x)
        self.entry_party_code.pack(side=tk.RIGHT, expand=True, padx=10, pady=5)
        ttk.Label(x, text="State Code:").pack(
            side=tk.RIGHT, expand=True, padx=10, pady=5)
        x.pack()

        ''' GOODS FORM / LISTBOX '''

        ttk.Label(self.window, text="GOODS", font=(
            "Arial", 11, "bold")).pack(expand=True)
        self.goods_table = goods_table.Table(self.window)

        ''' Purchase / Sale option '''
        x = ttk.Frame(self.bottom_left_frame)
        self.purchase_radio_button = ttk.Radiobutton(
            x, text="Purchase", variable=self.typeVar, value=True)
        self.purchase_radio_button.pack(
            side=tk.LEFT, expand=True, padx=10, pady=5)

        self.sale_radio_button = ttk.Radiobutton(
            x, text="Sale", variable=self.typeVar, value=False)
        self.sale_radio_button.pack(
            side=tk.RIGHT, expand=True, padx=10, pady=5)
        x.pack()

        x = ttk.Frame(self.bottom_left_frame)
        ttk.Label(x, text="Rs. in Words:").pack(
            side=tk.LEFT, expand=True, padx=10, pady=5)
        self.entry_rs_in_words = ScrolledText(
            x, height=2, width=48, wrap=tk.WORD)
        self.entry_rs_in_words.pack(
            side=tk.RIGHT, expand=True, padx=10, pady=5)
        x.pack(anchor="e")

        x = ttk.Frame(self.bottom_left_frame)
        ttk.Label(x, text="Bank Name:").pack(
            side=tk.LEFT, expand=True, padx=10, pady=5)
        self.entry_bank_name = ttk.Entry(x)
        self.entry_bank_name.pack(side=tk.RIGHT, expand=True, padx=10, pady=5)
        x.pack(anchor="e")

        x = ttk.Frame(self.bottom_left_frame)
        ttk.Label(x, text="A/c No.:").pack(side=tk.LEFT,
                                           expand=True, padx=10, pady=5)
        self.entry_ac_no = ttk.Entry(x)
        self.entry_ac_no.pack(side=tk.RIGHT, expand=True, padx=10, pady=5)
        x.pack(anchor="e")

        x = ttk.Frame(self.bottom_left_frame)
        ttk.Label(x, text="IFS Code:").pack(
            side=tk.LEFT, expand=True, padx=10, pady=5)
        self.entry_ifsc = ttk.Entry(x)
        self.entry_ifsc.pack(side=tk.RIGHT, expand=True, padx=10, pady=5)
        x.pack(anchor="e")

        x = ttk.Frame(self.bottom_right_frame)
        ttk.Label(x, text="Total Before Tax:").pack(
            side=tk.LEFT, expand=True, padx=10, pady=5)
        self.entry_total_before_tax = ttk.Entry(x)
        self.entry_total_before_tax.pack(
            side=tk.RIGHT, expand=True, padx=10, pady=5)
        x.pack(anchor="e")

        x = ttk.Frame(self.bottom_right_frame)
        self.sgst_var = tk.StringVar(x)
        self.sgst_var.set("SGST @" + str(self.SETTINGS['sgst']) + '%: ')
        self.label_sgst = ttk.Label(x, textvariable=self.sgst_var).pack(
            side=tk.LEFT, expand=True, padx=10, pady=5)
        self.entry_sgst = ttk.Entry(x)
        self.entry_sgst.pack(side=tk.RIGHT, expand=True, padx=10, pady=5)
        x.pack(anchor="e")

        x = ttk.Frame(self.bottom_right_frame)
        self.cgst_var = tk.StringVar(x)
        self.cgst_var.set("CGST @" + str(self.SETTINGS['cgst']) + '%: ')
        self.label_cgst = ttk.Label(x, textvariable=self.cgst_var).pack(
            side=tk.LEFT, expand=True, padx=10, pady=5)
        self.entry_cgst = ttk.Entry(x)
        self.entry_cgst.pack(side=tk.RIGHT, expand=True, padx=10, pady=5)
        x.pack(anchor="e")

        x = ttk.Frame(self.bottom_right_frame)
        self.igst_var = tk.StringVar(x)
        self.igst_var.set("IGST @" + str(self.SETTINGS['igst']) + '%: ')
        self.label_igst = ttk.Label(x, textvariable=self.igst_var).pack(
            side=tk.LEFT, expand=True, padx=10, pady=5)
        self.entry_igst = ttk.Entry(x)
        self.entry_igst.pack(side=tk.RIGHT, expand=True, padx=10, pady=5)
        x.pack(anchor="e")

        x = ttk.Frame(self.bottom_right_frame)
        ttk.Label(x, text="Total Tax Amount:").pack(
            side=tk.LEFT, expand=True, padx=10, pady=5)
        self.entry_total_tax_amt = ttk.Entry(x)
        self.entry_total_tax_amt.pack(
            side=tk.RIGHT, expand=True, padx=10, pady=5)
        x.pack(anchor="e")

        x = ttk.Frame(self.bottom_right_frame)
        ttk.Label(x, text="Total After Tax Amount:").pack(
            side=tk.LEFT, expand=True, padx=10, pady=5)
        self.entry_total_after_tax_amt = ttk.Entry(x)
        self.entry_total_after_tax_amt.pack(
            side=tk.RIGHT, expand=True, padx=10, pady=5)
        x.pack(anchor="e")

        x = ttk.Frame(self.bottom_right_frame)
        ttk.Label(x, text="GST on Reverse Charges:").pack(
            side=tk.LEFT, expand=True, padx=10, pady=5)
        self.entry_gst_reverse_charge = ttk.Entry(x)
        self.entry_gst_reverse_charge.pack(
            side=tk.RIGHT, expand=True, padx=10, pady=5)
        x.pack(anchor="e")

        self.entry_invoice_date.bind("<1>", self.calOpen)

        ''' Refresh Page '''
        self.btn_deets_calculate = ttk.Button(
            self.footer_frame, text='Refresh Page', command=self.onRefresh, width=30)
        self.btn_deets_calculate.grid(row=1, column=0, padx=10, pady=14)

        ''' Calculate Button '''
        self.btn_deets_calculate = ttk.Button(
            self.footer_frame, text='Calculate', command=self.onCalculate, width=30)
        self.btn_deets_calculate.grid(row=2, column=0, padx=10, pady=14)

        ''' Submit Button'''
        self.btn_invoice_submit = ttk.Button(
            self.footer_frame, text="Submit", command=self.onSubmit, width=30)
        self.btn_invoice_submit.grid(row=3, column=0, padx=10, pady=14)

        self.btn_invoice_print = ttk.Button(
            self.footer_frame, text='Print', command=self.onPrint, width=30)
        self.btn_invoice_print.grid(row=4, column=0, padx=10, pady=14)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.window.mainloop()
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?", master=self.window):
            try:
                self.main_window.destroy()
            except:
                pass
            self.window.destroy()
    
    def calOpen(self, event):
        datepick.CalWindow(self.dating)

    def insertInvoice(self):
        resp = createInvoice(self.invoice_data)
        print("Create invoice response:", resp)
        return resp

    def insertDetails(self, inv_id):
        self.goods_details = self.goods_table.getGoodsDetails()

        errors = 0
        for deet in self.goods_details:
            deet["invoice_id"] = inv_id
            x = models.createDetails(deet)
            if not x:
                errors += 1
        print("Errors:", errors)
        return True

    def performCaluclations(self):
        try:
            igst = int(self.SETTINGS["igst"])
            cgst = int(self.SETTINGS["cgst"])
            sgst = int(self.SETTINGS["sgst"])

            self.goods_details = self.goods_table.getGoodsDetails()
            # print(self.goods_details)
            j = 0
            total = 0
            for i in self.goods_details:

                ''' check for null '''
                for field in i:
                    if i[field] == "" or not i[field]:
                        continue

                ''' continue '''
                if i['Sr_No'] != '':
                    i['taxable_amt'] = float(i['qty']) * float(i['rate'])
                    total = total + i['taxable_amt']

                    # print(self.goods_table.entries[j])
                    # print(self.goods_table.entries[j]['total'].set(i['total']))
                    # self.goods_table.entries[j]['total'].set(i['total'])

                    self.goods_table.entries[j]['taxable_amt'].set(
                        float(i['qty']) * float(i['rate']))
                    j = j + 1

            ''' clear fields before inserting '''
            self.entry_rs_in_words.delete("1.0", END)
            self.entry_total_before_tax.delete(0, END)
            self.entry_cgst.delete(0, END)
            self.entry_igst.delete(0, END)
            self.entry_sgst.delete(0, END)
            self.entry_total_tax_amt.delete(0, END)
            self.entry_total_after_tax_amt.delete(0, END)

            self.entry_total_before_tax.insert(0, round(total, 2))
            self.entry_cgst.insert(0, round(total * cgst / 100, 2))
            self.entry_igst.insert(0, round(total * igst / 100, 2))
            self.entry_sgst.insert(0, round(total * sgst / 100, 2))

            self.entry_total_tax_amt.insert(
                0, round(total * ((cgst + sgst + igst) / 100), 2))
            self.entry_total_after_tax_amt.insert(
                0, round(total + (total * ((cgst + sgst + igst)) / 100), 2))

            words_before_point = num2words(self.entry_total_after_tax_amt.get()[
                :self.entry_total_after_tax_amt.get().index('.')])
            words_after_point = num2words(self.entry_total_after_tax_amt.get()[
                self.entry_total_after_tax_amt.get().index('.') + 1:]).replace("and ", "")
            words = (words_before_point + ' rupees and ' +
                     words_after_point + ' paise only.').title()
            self.entry_rs_in_words.insert("0.0", words)

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
                messagebox.showinfo(
                    title='Invoice Status', message='Invoice and details have been successfully recorded', master=self.window)
                return True

    def onRefresh(self):
        path = 'settings.json'
        with open(path) as f:
            self.SETTINGS = json.load(f)
        self.sgst_var.set("SGST @" + str(self.SETTINGS["sgst"]) + '%: ')
        self.cgst_var.set("CGST @" + str(self.SETTINGS["cgst"]) + '%: ')
        self.igst_var.set("IGST @" + str(self.SETTINGS["igst"]) + '%: ')

    def onCalculate(self):
        global CAL_CLICKED
        CAL_CLICKED += 1
        self.performCaluclations()
        if not self.validateData():
            self.sendAlert("Invalid Data! Should not contain any empty fields")

    def onSubmit(self):
        if CAL_CLICKED >= 1:
            if not self.validateData():
                self.sendAlert(
                    "Invalid Data! Should not contain any empty fields")
                return False
            msg_box = messagebox.askyesno(
                title='Attention', message="Are you sure, you want to submit? ", master=self.window)
            if msg_box:
                res = self.onConfirm()
                if not res:
                    self.sendAlert("Error while creating.")

        else:
            messagebox.showerror(
                title='Attention', message='Please click calculate button before submission', master=self.window)
        self.set_invoice_id()

    def collect_field_data(self):
        self.invoice_data = {
            "invoice_no":          self.entry_invoice_no.get(),
            "invoice_date":        datetime.strptime(self.entry_invoice_date.get(), '%d/%m/%Y'),
            "reverse_charges":     self.reverse_charge_var.get(),
            "state":               self.entry_party_state.get(),
            "state_code":          self.entry_party_code.get(),

            "name":                self.entry_party_name.get(),
            "address":             self.entry_party_address.get('1.0', 'end-1c'),
            "gst":                 self.entry_party_gstin.get(),
            "party_state":         self.entry_party_state.get(),
            "party_code":          self.entry_party_code.get(),

            "purchase":            self.typeVar.get(),
            "rupees_in_words":     self.entry_rs_in_words.get('1.0', 'end-1c'),
            "bank_name":           self.entry_bank_name.get(),
            "account_no":          self.entry_ac_no.get(),
            "ifsc":                 self.entry_ifsc.get(),

            "total_before_tax":    self.entry_total_before_tax.get(),
            "total_igst":          self.entry_igst.get(),
            "total_cgst":          self.entry_cgst.get(),
            "total_sgst":          self.entry_sgst.get(),
            "total_tax_amt":       self.entry_total_tax_amt.get(),
            "total_after_tax":     self.entry_total_after_tax_amt.get(),
            "gst_reverse_charge":  self.entry_gst_reverse_charge.get(),
        }

    def collect_goods_details_data(self):
        pass

    def onPrint(self):
        global CAL_CLICKED
        if CAL_CLICKED >= 1:
            if self.validateData() == True:
                self.onCalculate()
                self.collect_field_data()
                good_deets = self.goods_table.getGoodsDetails()
                # print(good_deets)
                filepath = filedialog.askdirectory(
                    initialdir=self.SETTINGS["default_save_folder"], title="Select a folder to export to", master=self.window)
                print(filepath)

                printing = create_invoice_pdf(
                    self.invoice_data, good_deets, filepath, self.SETTINGS)

                if printing:
                    messagebox.showinfo(
                        title='Print Status', message='PDF Generated Successfully', master=self.window)
                else:
                    messagebox.showerror(
                        title='Print Status', message='PDF could not be generated', master=self.window)
                print("Export to PDF response:", printing)
            else:
                messagebox.showerror(
                    title='Print Status', message='PDF could not be generated on invalid fields', master=self.window)
                return
        else:
            messagebox.showerror(
                title='Print Status', message='PDF could not be generated before calculation.', master=self.window)

    def validateData(self):
        goods_details = self.goods_table.getGoodsDetails()
        if goods_details == []:
            return False
        return True

    def sendAlert(self, message):
        messagebox.showerror(
            title='Error', message=message, master=self.window)

    def autofill_entity_fields(self):
        res = models.get_entity_by_name(self.autofill_var.get())
        if res == None:
            messagebox.showerror(
                title='Error', message='No saved items were found.', master=self.window)
            return
        x = {field: res.__dict__[field] for field in res.__dict__}
        # print(x)

        try:
            self.entry_party_name.delete(0, tk.END)
            self.entry_party_name.insert(0, x["name"])

            self.entry_ifsc.delete(0, tk.END)
            self.entry_ifsc.insert(0, x["ifc_code"])

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

    def set_invoice_id(self):
        try:
            x = models.get_last_invoice()
            if not x:
                return
            else:
                self.invoice_number_default.set(x)
        except Exception as e:
            print(e)
            self.back_to_home()
            return

    def back_to_home_page(self):
        self.window.destroy()

        