import tkinter as tk
from models import get_all_invoices, Invoice


class InvoiceTable:
    def __init__(self, window, invoices):
        fields = [column.key for column in Invoice.__table__.columns]
        
        ''' header row '''
        col = 0
        for f in fields:
            self.e = tk.Entry(window, width=12)
            self.e.grid(row = 0, column = col) 
            self.e.insert(tk.END, str(f))
            col += 1

        ''' data rows '''
        for i in range(len(invoices)):
            invoice = invoices[i].__dict__
            col = 0
            for field in fields:
                self.e = tk.Entry(window, width=12)
                self.e.grid(row = i + 1, column = col) 
                self.e.insert(tk.END, str(invoice[field]))
                col += 1


class ViewInvoiceWindow:
    def __init__(self):

        try:
            print("Fetching invoices...")
            self.invoices = get_all_invoices()
        except Exception as e:
            print(e)
            return

        self.window = tk.Tk()
        self.window.configure(background = "#f3f3f3")
        self.window.title("Home")
        self.window.geometry("1000x600")
        self.window.resizable(False, False)

        tk.Label(
            self.window, text = "Invoices"
        ).pack()

        self.dataframe = tk.Frame(
            self.window, width = 1000, height = 300
        )
        self.dataframe.pack()

        T = InvoiceTable(self.dataframe, self.invoices)
        
        self.window.mainloop()
    
    
        '''self.scrollbar_y = tk.Scrollbar(self.dataframe)
        self.scrollbar_y.pack(side = tk.RIGHT, fill = tk.Y)
        self.scrollbar_x = tk.Scrollbar(self.dataframe, orient = tk.HORIZONTAL)
        self.scrollbar_x.pack(side = tk.BOTTOM, fill = tk.X)

        self.invoice_listbox = tk.Listbox(
            self.dataframe, width = 140, height = 30,
            yscrollcommand = self.scrollbar_y.set,
            xscrollcommand = self.scrollbar_x.set
        )
        
        ### INSERT DATA 

        for i in self.invoices:
            x = i.__dict__.__str__()
            self.invoice_listbox.insert(
                tk.END, x
            )


        self.invoice_listbox.pack(side = tk.LEFT, fill = tk.BOTH)

        self.scrollbar_y.config(command = self.invoice_listbox.yview)
        self.scrollbar_x.config(command = self.invoice_listbox.xview)
        '''