from tkinter import *
import tkinter.messagebox
from models import Details


class Table:

    def __init__(self, root):

        f = Frame(root)
        # code for creating table
        # gets the cols
        self.titles = [column.key for column in Details.__table__.columns]

        self.entries = []

        ''' HEADER ROW '''

        col = 0
        for field in self.titles:
            self.i = Entry(f, width=12, font=('Arial', 10,))
            self.i.insert(END, field.replace("_", " ").title())
            self.i.config(state='readonly')
            self.i.grid(row=0, column=col)
            col += 1

        ''' create dict '''
        for row in range(8):
            x = {}
            for field in self.titles:
                x[field] = StringVar(root)

            self.entries.append(x)

            col = 0
            for field in self.titles:

                en = Entry(f, width=12, font=(
                    'Arial', 10,), textvariable=self.entries[row][field])
                en.grid(row=row + 1, column=col)
                col += 1

        f.place(x=100, y=200)
        # print(self.entries)

    def getGoodsDetails(self):
        for row in range(len(self.entries)):
            txn = {key: None for key in self.titles}
            for field in self.entries[row]:
                txn[field] = self.entries[row][field].get()
            print(txn)

        
