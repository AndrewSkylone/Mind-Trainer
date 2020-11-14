import tkinter as tk


EXERCISE_NAME = 'Диалоги'

class Exercise(tk.Frame):
    def __init__(self, master, cnf={}, **kw):
        tk.Frame.__init__(self, master, cnf, **kw)

        self.configure(bg='#e0ffff')

        self.create_widgets()
    
    def create_widgets(self):
        name_label = tk.Label(self, text=EXERCISE_NAME, fg=('Arial 16 bold'))
        name_label.grid(sticky='wesn')
