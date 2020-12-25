import tkinter as tk
from tkinter import filedialog
from importlib import reload
import os
import random

import exercise
reload(exercise)


class Exercise(exercise.Exercise_Frame):
    name = 'Фразы'

    def __init__(self, master, main_menu, cnf={}, **kw):
        exercise.Exercise_Frame.__init__(self, master, main_menu, cnf, **kw)

    def get_phrases_from_file(self) -> list:
        file_path = filedialog.askopenfilename(initialdir=os.path.dirname(__file__),
                                                title="Select file", filetypes=(("txt files", "*.txt"), ))
        folder = os.path.dirname(__file__)

        with open(os.path.join(folder, file_path), encoding='utf-8') as f:
            phrases = f.read().split('\n')
        return phrases
    
    def insert_phrase_in_text_area(self, phrase):
        raise NotImplementedError
    
    def start_training(self):
        raise NotImplementedError
    
    def check_phrase(self, phrase):
        raise NotImplementedError
    
    def next_phrase(self):
        if len(self.unlearned_phrases) == 0:
            self.start_training()
            return

        phrase = random.choice(self.unlearned_phrases)
        self.unlearned_phrases.remove(phrase)
        self.learned_phrases.append(phrase)

        self.display_var.set(phrase)

        self.update_counts()

        self.master.focus()
    
