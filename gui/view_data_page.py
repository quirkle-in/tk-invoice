from pdf_generation.create_invoice_pdf import create_invoice_pdf
from pdf_generation.purchase_sale_view import purchase_report
from tkinter import messagebox, ttk, filedialog
from gui.components import datepick
from ttkthemes import ThemedStyle
import tkinter as tk
import models


INVOICE_COLUMNS = [
    "invoice_id", "invoice_no", "invoice_date", "name", "address", "gst",
    "purchase", "account_no", "total_tax_amt", "total_after_tax"
]

DETAIL_COLUMNS = [
    "deet_id", "Sr_No", "invoice_id", "hsn", "prod", "batch_no", "mfg_date",
    "qty", "rate", "mrp", "taxable_amt"
]

ENTITY_COLUMNS = [
    "entity_id", "name", "address", "gstin_uid", "state",
    "state_code", "bank_name", "a_c_no", "ifc_code"
]


class TableView:

    def __init__(self, root, data, filters):
        self.root = root
        self.data = data

        self.base_frame = ttk.Frame(self.root)
        self.base_frame.pack(side=tk.BOTTOM, pady=20)

        self.canvas = tk.Canvas(self.base_frame, width=980, height=300)
        self.scrollbar_y = ttk.Scrollbar(
            self.base_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.frame = ttk.Frame(self.canvas)

        self.frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.frame, anchor="center")
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        if not self.data or self.data == []:
            ttk.Label(self.frame, text="No data found").pack(
                side=tk.TOP, padx=10, pady=10)
            return

        if filters["table"].get() == "Invoices":
            self.columns = INVOICE_COLUMNS
        elif filters["table"].get() == "Details":
            self.columns = DETAIL_COLUMNS
        else:
            self.columns = ENTITY_COLUMNS

        col = 0
        for field in self.columns:
            i = tk.Text(self.frame, width=12, height=2,
                        font=('Arial', 9, "bold"), wrap=tk.WORD)
            i.tag_configure('tag-center', justify='center')
            i.insert(tk.END, field.replace("_", " ").upper(), 'tag-center')
            i.configure(state="disabled")
            i.grid(row=0, column=col)
            col += 1

        for row in range(len(self.data)):
            x = self.data[row]
            # print(x)
            col = 0
            for field in self.columns:
                en = tk.Text(self.frame, width=12, height=2,
                             font=('Arial', 9), wrap=tk.WORD)
                en.insert(tk.END, str(x[field]))
                en.configure(state="disabled")
                en.grid(row=row + 1, column=col)
                col += 1


class ViewDataPage:
    def __init__(self, SETTINGS, main_window):
        self.SETTINGS = SETTINGS
        self.main_window = main_window

        self.window = tk.Tk()
        self.window.configure(background="#f3f3f3")
        self.window.title("View Page")
        self.window.geometry("1200x700")
        self.window.resizable(True, True)
        self.data = None

        self.DATA_TABLE = None

        self.filters = {
            "table": tk.StringVar(self.window, None),
            "limit": tk.StringVar(self.window, None),
            "type": tk.StringVar(self.window, None),
        }

        style = ThemedStyle(self.window)
        style.set_theme("breeze")
        self.window.iconbitmap('favicon.ico')

        self.header_frame = ttk.Frame(self.window)
        self.header_frame.pack(side=tk.TOP, padx=10, pady=10)

        self.title = ttk.Label(
            self.header_frame, text="VIEW & EXPORT DATA", font=("Arial", 14, "bold"))
        self.title.pack(side=tk.TOP, padx=300, pady=20)

        self.back_to_home = ttk.Button(
            self.header_frame, text="Back",
            command=self.back_to_home_page
        )
        self.back_to_home.pack(side=tk.LEFT)

        ''' FILTER FRAME '''

        self.filter_frame = ttk.Frame(
            self.window, borderwidth=2, relief="groove")
        self.filter_frame.pack(padx=20, pady=20)

        ttk.Label(self.filter_frame, text="Select Table: ").grid(
            row=0, column=0, padx=20)
        self.filter_table = ttk.OptionMenu(
            self.filter_frame, self.filters["table"], "None Selected", "None Selected", "Details", "Invoices", "Entities")
        self.filter_table.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.filter_frame, text="Type: ").grid(
            row=0, column=2, padx=20)
        self.filter_type = ttk.OptionMenu(
            self.filter_frame, self.filters["type"], "All", "Purchases", "Sales", "All")
        self.filter_type.grid(row=0, column=3, padx=10, pady=10)

        self.btn_execute = ttk.Button(
            self.filter_frame, text="Get Data / Refresh",
            command=self.get_view
        )
        self.btn_execute.grid(row=0, column=4, padx=20, pady=10)

        self.bottom_frame = ttk.Frame(
            self.window, borderwidth=2, relief="groove")
        self.bottom_frame.pack(side=tk.BOTTOM, expand=True, padx=10, pady=10)

        ''' DELETE DATA '''
        self.delete_frame = ttk.Frame(
            self.bottom_frame, borderwidth=2, relief="groove")
        self.delete_frame.pack(side=tk.RIGHT, padx=20, pady=20)

        ttk.Label(self.delete_frame, text="DELETE DATA").pack(
            side=tk.TOP, expand=True, padx=10, pady=10)

        self.table_delete = ttk.OptionMenu(
            self.delete_frame, self.filters["table"], "None Selected", "None Selected", "Details", "Invoices", "Entities")
        self.table_delete.pack(side=tk.LEFT, expand=True,  padx=10, pady=10)

        self.delete_id = tk.IntVar(self.delete_frame, value=1)
        self.entry_delete = ttk.Entry(
            self.delete_frame, textvariable=self.delete_id)
        self.entry_delete.pack(side=tk.LEFT, expand=True, padx=10, pady=10)

        self.btn_delete = ttk.Button(
            self.delete_frame, text="Delete", width=30, command=self.delete_table_row)
        self.btn_delete.pack(side=tk.LEFT, expand=True, padx=10, pady=10)

        ''' PRINT DATA '''
        self.print_frame = ttk.Frame(
            self.bottom_frame, borderwidth=2, relief="groove")
        self.print_frame.pack(side=tk.LEFT, padx=20, pady=20)

        ttk.Label(self.print_frame, text="PRINT DATA").pack(
            side=tk.TOP, expand=True, padx=10, pady=10)

        self.print_table = tk.StringVar(self.print_frame)
        self.table_print = ttk.Label(self.print_frame, text='Invoice ID:')
        self.table_print.pack(side=tk.LEFT, expand=True,  padx=10, pady=10)

        self.print_id = tk.IntVar(self.print_frame, value=1)
        self.entry_print = ttk.Entry(
            self.print_frame, textvariable=self.print_id)
        self.entry_print.pack(side=tk.LEFT, expand=True, padx=10, pady=10)

        self.btn_print = ttk.Button(
            self.print_frame, text="Print", width=30, command=self.print_table_row)
        self.btn_print.pack(side=tk.LEFT, expand=True, padx=10, pady=10)

        self.report_frame = ttk.Frame(
            self.window, borderwidth=2, relief="groove")
        self.report_frame.pack(side=tk.BOTTOM, padx=10, pady=10)

        self.var_start_date = tk.StringVar(self.window, value="All")
        self.var_end_date = tk.StringVar(self.window, value="All")

        ttk.Label(self.report_frame, text="Start Date").pack(
            side=tk.LEFT, expand=True, padx=10, pady=10)
        self.entry_start_date = ttk.Entry(
            self.report_frame, textvariable=self.var_start_date)  # date picker
        self.entry_start_date.pack(side=tk.LEFT, expand=True, padx=10, pady=5)
        #self.entry_start_date.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.entry_start_date.bind("<1>", self.calOpen_start)

        ttk.Label(self.report_frame, text="End Date").pack(
            side=tk.LEFT, expand=True, padx=10, pady=10)
        self.entry_end_date = ttk.Entry(
            self.report_frame, textvariable=self.var_end_date)  # date picker
        self.entry_end_date.pack(side=tk.LEFT, expand=True, padx=10, pady=5)
        #self.entry_end_date.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.entry_end_date.bind("<1>", self.calOpen_end)

        self.btn_purchases_report = ttk.Button(
            self.report_frame, text="Generate Purchases Report", width=30, command=self.generate_purchase_report)
        self.btn_purchases_report.pack(side=tk.LEFT, padx=10, pady=10)

        self.btn_sales_report = ttk.Button(
            self.report_frame, text="Generate Sales Report", width=30, command=self.generate_sales_report)
        self.btn_sales_report.pack(side=tk.LEFT, padx=10, pady=10)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.window.mainloop()
        
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?", master=self.window):
            try:
                self.main_window.destroy()
            except:
                pass
            self.window.destroy()

    def calOpen_start(self, event):
        datepick.CalWindow(self.var_start_date)

    def calOpen_end(self, event):
        datepick.CalWindow(self.var_end_date)

    def generate_purchase_report(self):
        details = models.purchase_report(
            self.var_start_date.get(), self.var_end_date.get())
        filepath = filedialog.askdirectory(
            master=self.window, initialdir=self.SETTINGS["default_save_folder"], title='Select Folder')
        DETAILS = {
            'path': filepath,
            'name': 'PURCHASE REPORT',
            'dets': details,
            "start_date": self.var_start_date.get().replace("/", "-"),
            "end_date": self.var_end_date.get().replace("/", "-")
        }
        status = purchase_report(DETAILS, self.SETTINGS)
        if status:
            messagebox.showinfo(
                title='Status', message='Purchase Report created successfully', master=self.window)
        else:
            messagebox.showerror(
                title='Error', message='Error during creation of Purchase Report', master=self.window)

    def generate_sales_report(self):
        details = models.sales_report(
            self.var_start_date.get(), self.var_end_date.get())
        filepath = filedialog.askdirectory(
            master=self.window, initialdir=self.SETTINGS["default_save_folder"], title='Select Folder')
        DETAILS = {
            'path': filepath,
            'name': 'SALES REPORT',
            'dets': details,
            "start_date": self.var_start_date.get().replace("/", "-"),
            "end_date": self.var_end_date.get().replace("/", "-")
        }
        status = purchase_report(DETAILS, self.SETTINGS)
        if status:
            messagebox.showinfo(
                title='Status', message='Sales Report created successfully', master=self.window)
        else:
            messagebox.showerror(
                title='Error', message='Error during creation of Sales Report', master=self.window)

    def get_view(self):
        filters = {i: self.filters[i].get() for i in self.filters}
        # print(filters)
        data = None

        if filters['table'] == 'None Selected':
            messagebox.showerror(
                title='Error', message='Select a table to get data from.', master=self.window)
            return

        data = models.filtered_view(
            filters["table"],
            filters["type"]
        )

        self.data = [{field: row.__dict__[field]
                      for field in row.__dict__} for row in data]

        try:
            if self.DATA_TABLE:
                self.DATA_TABLE.base_frame.destroy()
        except Exception as e:
            print(e)
        self.DATA_TABLE = TableView(self.window, self.data, self.filters)

    def print_table_row(self):
        _id = int(self.print_id.get())

        x = models.get_table_row(_id)
        if not x[0]:
            messagebox.showerror(
                "Attention", "You need to enter a valid invoice id.", master=self.window)
            return

        single_invoice = {
            "invoice_no":          x[0].invoice_no,
            "invoice_date":        x[0].invoice_date,
            "reverse_charges":     x[0].reverse_charges,
            "state":               x[0].state,
            "state_code":          x[0].state_code,

            "name":                x[0].name,
            "address":             x[0].address,
            "gst":                 x[0].gst,
            "party_state":         x[0].party_state,
            "party_code":          x[0].party_code,

            "purchase":            x[0].purchase,
            "rupees_in_words":     x[0].rupees_in_words,
            "bank_name":           x[0].bank_name,
            "account_no":          x[0].account_no,
            "ifsc":                x[0].ifsc,

            "total_before_tax":    x[0].total_before_tax,
            "total_igst":          x[0].total_igst,
            "total_cgst":          x[0].total_cgst,
            "total_sgst":          x[0].total_sgst,
            "total_tax_amt":       x[0].total_tax_amt,
            "total_after_tax":     x[0].total_after_tax,
            "gst_reverse_charge":  x[0].gst_reverse_charge
        }
        details = []
        s_no = 0
        for y in x[1]:
            details_dict = {
                'Sr_No': s_no,
                'prod': y.prod,
                'hsn': y.hsn,
                'batch_no': y.batch_no,
                'mfg_date': y.mfg_date,
                'qty': y.qty,
                'size': y.size,
                'rate': y.rate,
                'mrp': y.mrp,
                'taxable_amt': y.taxable_amt}
            details.append(details_dict)
            s_no += 1

        # print('Invoice Dets: ', single_invoice)
        # print('Details in inv: ', details)

        file_path = filedialog.askdirectory(
            initialdir=self.SETTINGS["default_save_folder"], title="Select a folder to export to", master=self.window)

        status = create_invoice_pdf(
            INVOICE=single_invoice, DETAILS=details, FILEPATH=file_path, SETTINGS=self.SETTINGS)

        if status:
            messagebox.showinfo(
                title='Status', message='PDF Generated', master=self.print_frame)
        else:
            messagebox.showerror(
                title='Error', message='Couldn\'t generate PDF', master=self.print_frame)

    def delete_table_row(self):
        table = self.filters["table"].get()
        _id = self.delete_id.get()

        #print('delete: ', table, _id)

        x = models.delete_table_row(table, _id)
        if x:
            return messagebox.showinfo("Success", "Deleted!", master=self.delete_frame)
        else:
            return messagebox.showerror("Error", "Could not delete", master=self.delete_frame)


    def back_to_home_page(self):
        self.window.destroy()
    
