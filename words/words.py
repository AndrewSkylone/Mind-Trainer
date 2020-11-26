import tkinter as tk
import os
import random
import copy
from tkinter import filedialog

EXERCISE_NAME = 'Слова'

class Exercise_Frame(tk.Frame):
    def __init__(self, master, cnf={}, **kw):
        tk.Frame.__init__(self, master, cnf, **kw)

        self.master = master
        self.bg = kw['bg']
        self.configure(bg=self.bg)

        self.word_var = tk.StringVar()
        file_path = filedialog.askopenfilename(initialdir=os.path.dirname(__file__),
                                                title="Select file", filetypes=(("txt files", "*.txt"), ))
        self.backup_words = self.read_words_from_file(file_name=file_path)
        self.words = copy.deepcopy(self.backup_words)

        self.create_widgets()

        self.next_world()
    
    def create_widgets(self):
        name_label = tk.Label(self, text=EXERCISE_NAME, font=('Arial 24 bold'), bg=self.bg)
        name_label.pack(fill=tk.X, side=tk.TOP, pady=10)

        #exercise frame
        exercise_frame = tk.Frame(self, bg=self.bg)
        exercise_frame.pack(fill=tk.Y, pady=20)

        self.word_entry = tk.Entry(exercise_frame, font='Arial 20 bold', bd=0, width=30, textvariable=self.word_var, justify='center')
        self.word_entry.grid(row=0, columnspan=3, pady=20)
        self.word_entry.bind('<Return>', lambda e: self.check_word(word=self.word_var.get()))

        self.count_label = tk.Label(exercise_frame, bg=self.bg, font='Arial 20 bold')
        self.count_label.grid(row=1, column=1)

        next_buton = tk.Button(exercise_frame, text='следующее', font=('Arial 16'), bg='#9cffe0', command=self.next_world)
        next_buton.grid(row=1, column=0, sticky='w')
        start_training_buton = tk.Button(exercise_frame, text='тренировка', font=('Arial 16'), bg='#9cffe0', command=self.start_training)
        start_training_buton.grid(row=1, column=2, sticky='e')

        self.text_area = tk.Text(exercise_frame, width=20, height=20)
        self.text_area.grid(row=2, columnspan=3, pady=10, sticky='swen')

    def check_word(self, word):
        for w in self.words:
            learning_word = w.split('(')[0]
            if self.get_strings_match_percent(word, learning_word) > 70:
                self.words.remove(w)
                self.count_label['text'] = len(self.words)
                self.word_var.set('')
                self.text_area.insert(tk.END, w + ', ')

    def get_strings_match_percent(self, string1, string2) -> int:
        str1_chars = set(string1.lower())
        str2_chars = set(string2.lower())

        union_str = str1_chars | str2_chars
        difference_str = str1_chars & str2_chars
        
        return int(len(difference_str) / len(union_str) * 100)

    def next_world(self):
        if len(self.words) == 0:
            self.start_training()
            return

        word = random.choice(self.words)
        self.word_var.set(word)
        self.word_entry.configure(bg=self.bg)
        self.words.remove(word)
        self.count_label['text'] = len(self.words)

        self.master.focus()

    def start_training(self):
        self.word_var.set('')
        self.word_entry.configure(bg='white')
        self.text_area.delete(1.0, tk.END)

        self.words = copy.deepcopy(self.backup_words)
        self.count_label['text'] = len(self.words)
        self.word_entry.focus()
    
    def read_words_from_file(self, file_name):
        words = []
        folder = os.path.dirname(__file__)
        with open(os.path.join(folder, file_name), encoding='utf-8') as f:
            words = f.read().split(',')
            words = [word.strip() for word in words]

        return words
