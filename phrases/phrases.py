import tkinter as tk
from tkinter import filedialog
from importlib import reload
import random
import os

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
        phrase = random.choice(self.learned_phrases)
        display_phrase = self.cut_phrase(phrase)[0]

        self.insert_display_text(text=display_phrase)
    
    def check_entered_phrase(self):
        entered_phrase = self.write_entry.get()
        full_training_phrase = self.get_full_displayed_phrase()
        training_phrase = self.cut_phrase(phrase=full_training_phrase)[1]

        if self.get_strings_match_percent(entered_phrase, training_phrase) > 70:
            self.phrase_is_right(phrase=full_training_phrase)
    