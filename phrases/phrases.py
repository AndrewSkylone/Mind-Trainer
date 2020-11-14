import tkinter as tk


EXERCISE_NAME = 'Фразы'

class Exercise_Frame(tk.Frame):
    def __init__(self, master, cnf={}, **kw):
        tk.Frame.__init__(self, master, cnf, **kw)

        self.master = master
        self.bg = kw['bg']
        self.configure(bg=self.bg)

        self.create_widgets()
    
    def create_widgets(self):
        name_label = tk.Label(self, text=EXERCISE_NAME, font=('Arial 16 bold'), bg=self.bg)
        name_label.pack(fill=tk.X, side=tk.TOP)
