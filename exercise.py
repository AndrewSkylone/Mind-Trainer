import tkinter as tk
from tkinter import filedialog
import copy
import os


class Exercise_Frame(tk.Frame):
    def __init__(self, master, main_menu, cnf={}, **kw):
        tk.Frame.__init__(self, master, cnf, **kw)

        self.main_menu = main_menu
        self.bg = kw['bg']
        self.configure(bg=self.bg)
        self.name = 'Exercise'
        self.display_var = tk.StringVar()
        self.write_entry = None

        # file_path = filedialog.askopenfilename(initialdir=os.path.dirname(__file__),
        #                                         title="Select file", filetypes=(("txt files", "*.txt"), ))
        # self.phrases_backup = self.get_phrases_from_file(file_name=file_path)
        # self.phrases = copy.deepcopy(self.phrases_backup)

        self.create_widgets()

        # self.next_phrase()
    
    def create_widgets(self):
        name_label = tk.Label(self, text=self.name, font=('Arial 24 bold'), bg=self.bg)
        name_label.pack(fill=tk.X, side=tk.TOP, pady=10)

        #exercise frame
        exercise_frame = tk.Frame(self, bg=self.bg)
        exercise_frame.pack(fill=tk.Y, pady=20)

        display_label = tk.Label(exercise_frame, font='Arial 14 bold', bg=self.bg, bd=0, width=30, textvariable=self.display_var, justify='center')
        display_label.grid(row=0, columnspan=4)

        self.write_entry = tk.Entry(exercise_frame, font='Arial 14 bold', bd=0, width=50, justify='center')
        self.write_entry.grid(row=1, columnspan=4, pady=10, sticky='w' + 'e')
        self.write_entry.bind('<Return>', lambda e: self.check_phrase(phrase=self.write_entry.get()))
        self.write_entry.bind('<Button-3>', lambda e: self.write_entry.delete(0, tk.END))

        next_buton = tk.Button(exercise_frame, text='следующее', font=('Arial 16'), bg='#9cffe0', command=self.next_phrase)
        next_buton.grid(row=2, column=0, sticky='w')

        self.learned_count_label = tk.Label(exercise_frame, bg=self.bg, font='Arial 18 bold')
        self.learned_count_label.grid(row=2, column=1, sticky='w')
        self.unlearned_count_label = tk.Label(exercise_frame, bg=self.bg, font='Arial 18 bold')
        self.unlearned_count_label.grid(row=2, column=2, sticky='e')

        start_training_buton = tk.Button(exercise_frame, text='тренировка', font=('Arial 16'), bg='#9cffe0', command=self.start_training)
        start_training_buton.grid(row=2, column=3, sticky='e')

        self.text_area = tk.Text(exercise_frame, width=20, height=15, font=('Arial 14'))
        self.text_area.grid(row=3, columnspan=4, pady=10, sticky='swen')

        menu_button = tk.Button(self, text='главное меню', font=('Arial 16'), bg='#e8e68b', command=self.main_menu.display_main_menu)
        menu_button.pack(side=tk.LEFT)

        quit_button = tk.Button(self, text='выход', font=('Arial 16'), bg='#e8e68b', command=self.main_menu.exit)
        quit_button.pack(side=tk.RIGHT)
    
    def get_strings_match_percent(self, string1, string2) -> int:
        s1 = string1.lower()
        s2 = string2.lower()        
        shorter_word = s1 if len(s1) <= len(s2) else s2
        longer_word = s2 if len(s2) >= len(s1) else s1
        
        difference_str = list(longer_word)
        for char in shorter_word:
            if char in difference_str:
                difference_str.remove(char)
        
        return 100 - int(len(difference_str) / len(string2) * 100)

    def start_training(self):
        raise NotImplementedError
    
    def check_phrase(self, phrase):
        raise NotImplementedError
    
    def next_phrase(self):
        raise NotImplementedError
    
    def get_phrases_from_file(self, file_name):
        raise NotImplementedError
