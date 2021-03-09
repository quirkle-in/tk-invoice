from models import get_all_invoices
from ttkthemes import ThemedStyle
from tkinter import ttk
import tkinter as tk


class TableView:

    def __init__(self, root, data):
        self.root = root
        self.data = data
        
        self.base_frame = ttk.Frame(self.root)
        self.base_frame.pack(side = tk.BOTTOM, padx=100, pady=20, fill=tk.BOTH)

        self.canvas = tk.Canvas(self.base_frame, width=1200, height = 300)
        self.scrollbar_y = ttk.Scrollbar(self.base_frame,
            orient = tk.VERTICAL, command = self.canvas.yview)
        self.scrollbar_x = ttk.Scrollbar(self.base_frame,
            orient = tk.HORIZONTAL, command = self.canvas.xview)
        self.frame = ttk.Frame(self.canvas, width=1200)

        self.frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion = self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)
        self.canvas.configure(xscrollcommand=self.scrollbar_x.set)

        self.canvas.pack(side="left", fill=tk.BOTH, expand=True)
        self.scrollbar_y.pack(side="right", fill = "y")
        self.scrollbar_x.pack(side="bottom", fill = "x")
        
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


class ViewDataPage:
    def __init__(self):

        self.window = tk.Tk()
        self.window.configure(background = "#f3f3f3")
        self.window.title("View Page")
        self.window.geometry("1200x700")
        self.window.resizable(True, True)

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


        data = get_all_invoices()
        V = TableView(self.window, data)

        self.window.mainloop()


    def back_to_home_page(self):
        ''' confirmation '''
        pass

        self.window.destroy()