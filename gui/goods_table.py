from sqlalchemy.ext.declarative import base
from models import Details
from tkinter import ttk
import tkinter as tk


class Table:

    def __init__(self, root):
        self.root = root
        self.total_goods_rows = 0


        self.base_frame = tk.Frame(self.root)
        #self.base_frame.grid(row = 1, column = 1)

        self.canvas = tk.Canvas(self.base_frame)
        #self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.pack(side = "left")

        self.f = tk.Frame(self.canvas)
        self.f.pack()

        self.scrollbar_y = tk.Scrollbar(self.base_frame, #canvas, maybe
            orient = "vertical", command = self.canvas.yview)
        self.scrollbar_y.pack(side = "right", fill = "y")
        # so is it done?  its not scrolling, frame / canvas keeps getting big
        # what if you just open a new window for more stuff? each row, new window?
        # set a limit of say 10 for og wind and then new
        # just [ut audio off, nou]

        self.canvas.config(yscrollcommand=self.scrollbar_y.set)

# what if we add scroll on frame rather canvas O, ohh ha sry, everywhere?
#can try that yes, can't use yview on a frame,

        # gets the cols
        self.titles = [column.key for column in Details.__table__.columns]
        self.titles.remove('invoice_id')
        self.entries = []

        ''' HEADER ROW '''

        col = 0
        for field in self.titles:
            self.i = ttk.Entry(self.f, width=14, font=('Arial', 9), 
                justify = tk.CENTER)
            self.i.insert(tk.END, field.replace("_", " ").upper())
            self.i.config(state='readonly')
            self.i.grid(row=0, column=col)
            col += 1

        ''' create dict '''
        for row in range(0):
            x = {}
            for field in self.titles:
                x[field] = tk.StringVar(root)

            self.entries.append(x)

            col = 0
            for field in self.titles:

                en = ttk.Entry(self.f, width=14, font=(
                    'Arial', 9,), textvariable=self.entries[self.total_goods_rows][field])
                en.grid(row=self.total_goods_rows + 1, column=col)
                col += 1
            self.total_goods_rows += 1

        '''for i in self.entries:
            print(type(i['total']))
            break'''
        
        self.btn_add_row = ttk.Button(
            self.root, text = "Add New Row",
            command = self.add_new_goods_row
        )
        self.btn_add_row.place(x = 600, y = 180)
        
        
    def getGoodsDetails(self):
        list_of_entries = []
        for row in range(len(self.entries)):
            txn = {key: None for key in self.titles}
            for field in self.entries[row]:
                txn[field] = self.entries[row][field].get()
            list_of_entries.append(txn)
        return list_of_entries

        
    def add_new_goods_row(self):
        x = {}
        for field in self.titles:
            x[field] = tk.StringVar(self.root)

        self.entries.append(x)

        col = 0
        for field in self.titles:

            en = ttk.Entry(self.f, width=14, font=('Arial', 9,),
                textvariable=self.entries[self.total_goods_rows][field])
            en.grid(row=self.total_goods_rows + 1, column=col)
            col += 1
        self.total_goods_rows += 1
    # if we implement scroll on base_frame itself? 
    # hmmmmm call take, can do th