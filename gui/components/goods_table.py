from sys import maxsize
from sqlalchemy.ext.declarative import base
from models import Details
from tkinter import ttk
import tkinter as tk


class Table:

    def __init__(self, root):
        self.root = root
        self.total_goods_rows = 0
        self.rows = []

        self.base_frame = ttk.Frame(self.root, borderwidth=2, relief="groove")
        self.base_frame.pack(padx=10)

        self.button_frame = ttk.Frame(self.base_frame)
        self.button_frame.pack(padx = 10, pady = 10, side=tk.BOTTOM)

        self.btn_add_row1 = ttk.Button(
            self.button_frame, text="Add Row: Madhusheel Plus",
            command=self.add_new_goods_row_m,
            width=30
        )
        self.btn_add_row1.pack(side=tk.LEFT)

        self.btn_add_row2 = ttk.Button(
            self.button_frame, text="Add Row: Ashrangi Capsule",
            command=self.add_new_goods_row_a,
            width=30
        )
        self.btn_add_row2.pack(side=tk.LEFT)

        self.btn_del_row = ttk.Button(
            self.button_frame, text="Delete Row",
            command=self.delete_goods_row,
            width=20
        )
        self.btn_del_row.pack(side=tk.LEFT) #where's the delete btn put that alososi n thatuat frame

        self.canvas = tk.Canvas(self.base_frame, width=960, height=120)
        self.scrollbar_y = ttk.Scrollbar(self.base_frame,  # canvas, maybe
                                         orient="vertical", command=self.canvas.yview)
        self.frame = ttk.Frame(self.canvas)

        self.frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar_y.pack(side="right", fill="y")

        # gets the cols
        self.titles = [column.key for column in Details.__table__.columns]
        self.titles.remove('deet_id')
        self.titles.remove('invoice_id')
        self.entries = []

        ''' HEADER ROW '''

        col = 0
        for field in self.titles:
            self.i = ttk.Entry(self.frame, width=14, font=('Arial', 8),
                               justify=tk.CENTER)
            self.i.insert(tk.END, field.replace("_", " ").upper())
            self.i.configure(state="disabled", foreground="#000000")
            self.i.grid(row=0, column=col)
            col += 1

        # for _ in range(1):
        #     self.add_new_goods_row()

    def getGoodsDetails(self):
        list_of_entries = []
        for row in self.entries:
            txn = {}
            valid = True
            for field in self.titles:
                x = row[field].get()
                if field not in ["total", "taxable_amt"]:
                    if x == "" or not x:

                        valid = False
                        break
                    txn[field] = row[field].get()
                else:
                    txn[field] = row[field].get()
            if valid:
                list_of_entries.append(txn)
        return list_of_entries
    
    def add_new_goods_row_m(self):
        self.add_new_goods_row(prod_type='Madhusheel Plus')

    def add_new_goods_row_a(self):
        self.add_new_goods_row(prod_type='Ashrangi Capsule')
    

    def add_new_goods_row(self, prod_type):
        x = {}
        for field in self.titles:
            x[field] = tk.StringVar(self.root)

        self.entries.append(x)

        col = 0
        for field in self.titles:
            if field == 'prod' and prod_type == 'Madhusheel Plus':
                self.entries[self.total_goods_rows][field].set(prod_type)
                en = ttk.Entry(self.frame, width=14, font=('Arial', 8),
                            textvariable=self.entries[self.total_goods_rows][field])
                en.grid(row=self.total_goods_rows + 1, column=col)
            elif field == 'prod' and prod_type == 'Ashrangi Capsule':
                self.entries[self.total_goods_rows][field].set(prod_type)
                en = ttk.Entry(self.frame, width=14, font=('Arial', 8),
                            textvariable=self.entries[self.total_goods_rows][field])
                en.grid(row=self.total_goods_rows + 1, column=col)
            else:
                en = ttk.Entry(self.frame, width=14, font=('Arial', 8),
                            textvariable=self.entries[self.total_goods_rows][field])
                en.grid(row=self.total_goods_rows + 1, column=col)
            self.rows.append(en)
            col += 1

        # default id
        self.entries[self.total_goods_rows]["Sr_No"].set(len(self.entries))
        self.total_goods_rows += 1

    def delete_goods_row(self):
        if len(self.rows) > 0:
            for i in range(10):
                self.rows[-1].destroy()
                self.rows.pop(-1)
            self.entries.pop(-1)
            self.total_goods_rows -= 1