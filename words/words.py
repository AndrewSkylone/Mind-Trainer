import tkinter as tk
import os
import random


EXERCISE_NAME = 'Слова'

class Exercise_Frame(tk.Frame):
    def __init__(self, master, cnf={}, **kw):
        tk.Frame.__init__(self, master, cnf, **kw)

        self.master = master
        self.bg = kw['bg']
        self.configure(bg=self.bg)

        self.words = self.read_words_from_file(file_name='words.txt')

        self.create_widgets()

        self.next_world()
    
    def create_widgets(self):
        name_label = tk.Label(self, text=EXERCISE_NAME, font=('Arial 24 bold'), bg=self.bg)
        name_label.pack(fill=tk.X, side=tk.TOP, pady=10)

        #exercise frame
        exercise_frame = tk.Frame(self, bg=self.bg)
        exercise_frame.pack(fill=tk.Y, pady=20)

        self.word_entry = tk.Entry(exercise_frame, font='Arial 20 bold', bd=0, width=40, justify='center')
        self.word_entry.textvariable = tk.StringVar()
        self.word_entry.configure(textvariable=self.word_entry.textvariable)
        self.word_entry.grid(row=0, columnspan=3, pady=20)

        self.count_label = tk.Label(exercise_frame, bg=self.bg, font='Arial 20 bold')
        self.count_label.grid(row=1, column=1)

        next_buton = tk.Button(exercise_frame, text='следующее', font=('Arial 16'), bg='#9cffe0', command=self.next_world)
        next_buton.grid(row=1, column=0, padx=5)
        start_training_buton = tk.Button(exercise_frame, text='тренировка', font=('Arial 16'), bg='#9cffe0', command=self.start_training)
        start_training_buton.grid(row=1, column=2, padx=5)

    def next_world(self):
        if len(self.words) == 0:
            self.start_training()
            return

        word = random.choice(self.words)
        self.word_entry.textvariable.set(word)
        self.word_entry.configure(bg=self.bg)
        self.words.remove(word)
        self.count_label['text'] = len(self.words)

    def start_training(self):
        pass
    
    def read_words_from_file(self, file_name):
        words = []
        folder = os.path.dirname(__file__)
        with open(os.path.join(folder, file_name), encoding='utf-8') as f:
            words = f.read().split(',')
            words = [word.strip() for word in words]

        return words
