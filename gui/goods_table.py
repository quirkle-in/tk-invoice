from sys import maxsize
from sqlalchemy.ext.declarative import base
from models import Details
from tkinter import ttk
import tkinter as tk


class Table:

    def __init__(self, root):
        self.root = root
        self.total_goods_rows = 0


        self.base_frame = ttk.Frame(self.root)
        self.base_frame.place(x=20, y=220)

        self.canvas = tk.Canvas(self.base_frame, width=940, height = 160)
        self.scrollbar_y = ttk.Scrollbar(self.base_frame, #canvas, maybe
            orient = "vertical", command = self.canvas.yview)
        self.frame = ttk.Frame(self.canvas)

        self.frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion = self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar_y.pack(side="right", fill = "y")


        # gets the cols
        self.titles = [column.key for column in Details.__table__.columns]
        self.titles.remove('deet_id')
        self.titles.remove('invoice_id')
        self.entries = []

        ''' HEADER ROW '''

        col = 0
        for field in self.titles:
            self.i = ttk.Entry(self.frame, width=13, font=('Arial', 9), 
                justify = tk.CENTER)
            self.i.insert(tk.END, field.replace("_", " ").upper())
            self.i.config(state='readonly')
            self.i.grid(row=0, column=col)
            col += 1
        
        self.btn_add_row = ttk.Button(
            self.root, text = "Add New Row",
            command = self.add_new_goods_row,
            width = 50
        )
        self.btn_add_row.place(x = 50, y = 185)

        for default_row in range(3):
            self.add_new_goods_row()
        
        
    def getGoodsDetails(self):
        list_of_entries = []
        for row in range(len(self.entries)):
            txn = {}
            for field in self.titles:
                txn[field] = self.entries[row][field].get()
            for i in txn:
                if txn[i] == "" or txn[i] == None:
                    continue
            list_of_entries.append(txn)
        return list_of_entries

        
    def add_new_goods_row(self):
        x = {}
        for field in self.titles:
            x[field] = tk.StringVar(self.root)

        self.entries.append(x)

        col = 0
        for field in self.titles:
            en = ttk.Entry(self.frame, width=13, font=('Arial', 9),
                textvariable=self.entries[self.total_goods_rows][field])
            en.grid(row=self.total_goods_rows + 1, column=col)
            col += 1
        
        ### default id
        self.entries[self.total_goods_rows]["deet_no"].set(len(self.entries))
        self.total_goods_rows += 1