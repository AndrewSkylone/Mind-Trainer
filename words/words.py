import tkinter as tk
from tkinter import filedialog
from importlib import reload
import random
import os
from datetime import datetime

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
            text = f.read()
            phrases = text.split(', ') if len(text.split(', ')) > len(text.split('\n')) else text.split('\n')

        return phrases

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