from tkinter import *


class Table:

    def __init__(self, root):

        f = Frame(root)
        # code for creating table
        titles = ['Sr No.', 'Name', 'HSN', 'Qty',
                  'Rate', 'MRP', 'Total', 'Disc', 'Taxable Value']
        for i in titles:
            self.i = Entry(f, width=12, font=('Arial', 10,))
            self.i.insert(0, i)
            self.i.config(state='readonly')
            self.i.grid(row=1, column=titles.index(i))
        for i in range(1, 9):
            for j in titles:
                self.i = Entry(f, width=12, font=('Arial', 10,))
                self.i.insert(0, str(i))
                self.i.grid(row=i + 1, column=titles.index(j))

        f.place(x=100, y=200)
