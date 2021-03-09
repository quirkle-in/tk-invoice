from ttkthemes import ThemedStyle
from tkinter import ttk
import tkinter as tk
import models

class TableView:

    def __init__(self, root, data):
        self.root = root
        self.data = data
        
        self.base_frame = ttk.Frame(self.root)
        self.base_frame.pack(side = tk.BOTTOM, padx=10, pady=20)

        self.canvas = tk.Canvas(self.base_frame, width=1150, height = 300)
        self.scrollbar_y = ttk.Scrollbar(self.base_frame,
            orient = tk.VERTICAL, command = self.canvas.yview)
        self.frame = ttk.Frame(self.canvas, width=1150)

        self.frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion = self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.frame, anchor="center")
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar_y.pack(side=tk.RIGHT, fill = tk.Y)
        
        if not self.data or self.data == []:
            return

        self.columns = [i.name for i in data[0].__table__.columns]
        
        col = 0
        for field in self.columns:
            i = tk.Text(self.frame, width=14, height = 2, font=('Arial', 8, "bold"), wrap = tk.WORD)
            i.tag_configure('tag-center', justify='center')
            i.insert(tk.END, field.replace("_", " ").upper(), 'tag-center')
            i.configure(state="disabled")
            i.grid(row=0, column=col)
            col += 1

        for row in range(len(self.data)):
            x = self.data[row].__dict__
            col = 0
            for field in self.columns:
                en = tk.Text(self.frame, width=14, height = 2, font=('Arial', 8), wrap = tk.WORD)
                en.insert(tk.END, x[field])
                en.configure(state="disabled")
                en.grid(row= row + 1, column=col)
                col += 1


class InvoiceView:
    def __init__(self, invoice, details):
        self.root = tk.Tk()

        self.invoice = invoice
        self.details = details
        
        self.base_frame = ttk.Frame(self.root)
        self.base_frame.pack(side = tk.BOTTOM, padx=20, pady=20)

        self.canvas = tk.Canvas(self.base_frame, width=1100, height = 300)
        self.scrollbar_y = ttk.Scrollbar(self.base_frame,
            orient = tk.VERTICAL, command = self.canvas.yview)
        self.frame = ttk.Frame(self.canvas, width=1100)

        self.frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion = self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.frame, anchor="center")
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar_y.pack(side=tk.RIGHT, fill = tk.Y)
        
        if not self.invoice:
            return
        
        self.invoice = self.invoice.__dict__
        
        col = 0
        for field in self.invoice:
            en = tk.Text(self.frame, width=14, height = 2, font=('Arial', 8), wrap = tk.WORD)
            en.insert(tk.END, field)
            en.configure(state="disabled")
            en.grid(row = 0, column=col)

            val = tk.Text(self.frame, width=14, height = 2, font=('Arial', 8), wrap = tk.WORD)
            val.insert(tk.END, self.invoice[field])
            val.configure(state="disabled")
            val.grid(row = 1, column=col)

            col += 1
        
        self.root.mainloop()



class ViewDataPage:
    def __init__(self):

        self.window = tk.Tk()
        self.window.configure(background = "#f3f3f3")
        self.window.title("View Page")
        self.window.geometry("1200x700")
        self.window.resizable(True, True)
        self.data = None
        self.DATA_TABLE = None

        
        self.filters = {
            "table" : tk.StringVar(self.window, "Invoice"),
            "limit": tk.StringVar(self.window, "")
        }

        style = ThemedStyle(self.window)
        style.set_theme("vista")

        self.title = ttk.Label(
            self.window, text="VIEW & EXPORT", font = ("Arial", 14, "bold")
        )
        self.title.pack(side=tk.TOP, padx=300, pady=50)

        self.back_to_home = ttk.Button(
            self.window, text="Back",
            command = self.back_to_home_page
        )
        self.back_to_home.pack(side=tk.TOP)

        ''' FILTER FRAME '''

        self.filter_frame = ttk.Frame(self.window)
        self.filter_frame.pack(padx=20, pady=20)

        self.filter_table = ttk.OptionMenu(
            self.filter_frame, self.filters["table"], "Invoices", "Details", "Invoices"
        )
        self.filter_table.grid(row = 0, column = 0)
        
        self.btn_execute = ttk.Button(
            self.filter_frame, text = "Get Data",
            command = self.get_view
        )
        self.btn_execute.grid(row = 0, column = 1)        

        self.btn_export = ttk.Button(
            self.window, text = "Export View",
            command = self.export_data_to_pdf,
            width=30
        )
        self.btn_export.pack(side = tk.BOTTOM, padx=20, pady = 20)

        self.window.mainloop()


    def back_to_home_page(self):
        ''' confirmation '''
        pass

        self.window.destroy()
    

    def get_view(self):
        table = self.filters["table"].get()
        
        data = None
        print( "Fetching data from ", table)

        if table == "Invoices":
            data = models.get_all_invoices()
        elif table == "Details":
            data = models.get_all_details()
        
        ''' filters '''

        self.data = data

        try:
            self.DATA_TABLE.base_frame.destroy()
        except:
            pass
        self.DATA_TABLE = TableView(self.window, self.data)


    def export_data_to_pdf(self):
        if self.data:
            return [
                {
                    field: row.__dict__[field] for field in row.__dict__
                } for row in self.data
            ]
