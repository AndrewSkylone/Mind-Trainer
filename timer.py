import tkinter as tk


class Timer_GUI(tk.Frame):
    def __init__(self, master, cnf={}, **kw):
        tk.Frame.__init__(self, master, cnf, **kw)

        self.__timer_label = None

        self.create_widgets()
    
    def create_widgets(self):
        self.__timer_label = tk.Label(self, text='00:00:00')
        self.__timer_label.grid()
    
    def set_time(self, time, color='green'):
        self.__timer_label.configure(text=time, color=color)
    
    def start_timer(self, time):
        for 