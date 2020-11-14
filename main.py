import tkinter as tk
from importlib import reload
import sys

from words import words
from phrases import phrases
from dialogs import dialogs


exercises_libs = {words : "#ffc9c9", phrases : '#e0ffff', dialogs : '#e1ffe0'}
BACKGROUNG = '#fff3d1'

class MainFrame(tk.Frame):
    def __init__(self, master, cnf={}, **kw):
        tk.Frame.__init__(self, master, cnf, **kw)

        self.master = master
        self.create_widgets()
    
    def create_widgets(self):
        menu_frame = tk.Frame(self)
        menu_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        menu_frame.configure(bg=BACKGROUNG)

        for index, lib in enumerate(exercises_libs.keys()):
            ex_button = tk.Button(menu_frame, text=lib.EXERCISE_NAME, width=20)
            ex_button.configure(font=('Arial 16'), bg=exercises_libs[lib])
            ex_button.configure(command=lambda lib=lib: self.create_exercise(exercise_lib=lib))
            ex_button.grid(row=index, pady=10, sticky='swen')
            
    def create_exercise(self, exercise_lib):
        self.pack_forget()

        reload(exercise_lib)
        self.exercise_frame = exercise_lib.Exercise_Frame(self.master, bg=exercises_libs[exercise_lib])
        self.exercise_frame.pack(fill=tk.BOTH, expand=True)

        panel_frame.configure(bg=exercises_libs[exercise_lib])

    def display(self):
        if hasattr(self, 'exercise_frame'):
            self.exercise_frame.destroy()
            del(self.exercise_frame)

            panel_frame.configure(bg=BACKGROUNG)

        self.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    
    root = tk.Tk()

    height = 600
    width = 700
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    
    root.geometry(f"{width}x{height}+{screen_w//2 - width//2}+{screen_h//2 - height//2}")
    root.resizable(False, False)
    root.title('Brain Trainer')

    #exercises frame
    exercises_frame = tk.Frame(root)
    exercises_frame.pack(fill=tk.BOTH, expand=True)

    main_frame = MainFrame(exercises_frame, bg=BACKGROUNG)
    main_frame.display()

    #panel frame
    panel_frame = tk.Frame(root, bg=BACKGROUNG)
    panel_frame.pack(fill=tk.BOTH)

    menu_button = tk.Button(panel_frame, text='главное меню', font=('Arial 16'), bg='#e8e68b', command=main_frame.display)
    menu_button.pack(side=tk.LEFT)

    quit_button = tk.Button(panel_frame, text='выход', font=('Arial 16'), bg='#e8e68b', command=sys.exit)
    quit_button.pack(side=tk.RIGHT)

    root.mainloop()
    
