import tkinter as tk
from importlib import reload
import sys

from words import words
from phrases import phrases
from dialogs import dialogs


exercises_libs = [words, phrases, dialogs]
BACKGROUNG = '#fff3d1'

class MainFrame(tk.Frame):
    def __init__(self, master, cnf={}, **kw):
        tk.Frame.__init__(self, master, cnf, **kw)

        self.create_widgets()
    
    def create_widgets(self):
        menu_frame = tk.Frame(self)
        menu_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        menu_frame.configure(bg='#a6e3af')

        for index, lib in enumerate(exercises_libs):
            ex_button = tk.Button(menu_frame, text=lib.EXERCISE_NAME,
                                    command=lambda lib=lib: self.create_exercise(exercise=lib.Exercise))
            ex_button.grid(row=index)
        
            
    def create_exercise(self, exercise):
        pass


if __name__ == "__main__":
    def reload_libs():
        for lib in exercises_libs:
            reload(lib)
    
    root = tk.Tk()

    height = 600
    width = 700
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    
    root.geometry(f"{width}x{height}+{screen_w//2 - width//2}+{screen_h//2 - height//2}")
    root.resizable(False, False)
    root.title('Brain Trainer')

    main_frame = MainFrame(root, bg=BACKGROUNG)
    main_frame.pack(fill=tk.BOTH, expand=True)

    panel_frame = tk.Frame(root, bg=BACKGROUNG)
    panel_frame.pack(fill=tk.BOTH)
    reload_button = tk.Button(panel_frame, text='reload', command=reload_libs)
    reload_button.pack(side=tk.LEFT)
    quit_button = tk.Button(panel_frame, text='quit', command=sys.exit)
    quit_button.pack(side=tk.RIGHT)

    root.mainloop()
    
