import tkinter as tk
from tkinter import filedialog
from importlib import reload
import random
import os

import exercise
reload(exercise)


class Exercise(exercise.Exercise_Frame):
    name = 'Слова'

    def __init__(self, master, main_menu, cnf={}, **kw):
        self.file_path = filedialog.askopenfilename(initialdir=os.path.dirname(__file__),
                                                title="Select file", filetypes=(("txt files", "*.txt"), ))
                                                
        exercise.Exercise_Frame.__init__(self, master, main_menu, cnf, **kw)

        self.word_var = tk.StringVar()
        self.word_var.trace('w', lambda *args: self.set_right_or_wrong_font())
        self.write_entry.config(textvariable=self.word_var)

    def get_phrases_from_file(self) -> list:
        folder = os.path.dirname(__file__)

        with open(os.path.join(folder, self.file_path), encoding='utf-8') as f:
            phrases = f.read().split(',')
            if len(phrases) == 1:
                f.seek(0)                
                phrases = f.read().split('\n')

        return phrases
    
    def start_training(self):
        phrase = random.choice(self.learned_phrases)
        display_phrase = self.cut_phrase(phrase)[1]

        self.insert_display_text(text=display_phrase)

    def check_entered_phrase(self):
        entered_phrase = self.write_entry.get()

        max_match_percent = 0
        max_match_phrase = ''
        
        for learned in self.learned_phrases:
            right_phrase = self.cut_phrase(phrase=learned)[0]
            match_percent = self.get_strings_match_percent(entered_phrase, right_phrase)
            if match_percent > max_match_percent:
                max_match_percent = match_percent
                max_match_phrase = learned

        if max_match_percent > 75:
            self.phrase_is_right(phrase=max_match_phrase)
        
    def cut_phrase(self, phrase) -> (str, str):
        splited_phrase = phrase.split(' - ')
        if len(splited_phrase) > 1:
            return splited_phrase[0], splited_phrase[1]

        splited_phrase = phrase.split('(')
        if len(splited_phrase) > 1:
            return splited_phrase[0], splited_phrase[1].replace(')', '')
        
        return phrase, ''
    
    def set_right_or_wrong_font(self):
        for phrase in self.learned_phrases:
            if self.word_var.get() in self.cut_phrase(phrase)[0]:
                self.write_entry.config(fg='black')
                return
        
        self.write_entry.config(fg='red')

class Exercise_Frame(tk.Frame):
    def __init__(self, master, cnf={}, **kw):
        tk.Frame.__init__(self, master, cnf, **kw)

        self.master = master
        self.bg = kw['bg']
        self.configure(bg=self.bg)

        self.word_var = tk.StringVar()
        self.word_var.trace('w', lambda *args: self.set_right_or_wrong_font())
        file_path = filedialog.askopenfilename(initialdir=os.path.dirname(__file__),
                                                title="Select file", filetypes=(("txt files", "*.txt"), ))
        self.backup_words = self.read_file(file_name=file_path)
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

        self.text_area = tk.Text(exercise_frame, width=20, height=15, font=('Arial 14'))
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
        s1 = string1.lower()
        s2 = string2.lower()        
        shorter_word = s1 if len(s1) <= len(s2) else s2
        longer_word = s2 if len(s2) >= len(s1) else s1
        
        difference_str = list(longer_word)
        for char in shorter_word:
            if char in difference_str:
                difference_str.remove(char)
        
        return 100 - int(len(difference_str) / len(string2) * 100)

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
    
    def read_file(self, file_name):
        folder = os.path.dirname(__file__)
        with open(os.path.join(folder, file_name), encoding='utf-8') as f:
            words = f.read().split(',')
            words = [word.strip() for word in words]

        return words

    def set_right_or_wrong_font(self):
        for word in self.words:
            if self.word_var.get() in word:
                self.word_entry.config(fg='black')
                return
        
        self.word_entry.config(fg='red')