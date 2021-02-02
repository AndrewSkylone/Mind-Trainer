import tkinter as tk
from tkinter import filedialog
from importlib import reload
import random
import os
from datetime import datetime

import exercise
reload(exercise)


class Exercise(exercise.Exercise_Frame):
    name = 'Диалоги'

    def __init__(self, master, main_menu, cnf={}, **kw):
        self.file_path = filedialog.askopenfilename(initialdir=os.path.dirname(__file__),
                                                title="Select file", filetypes=(("txt files", "*.txt"), ))
                                                
        exercise.Exercise_Frame.__init__(self, master, main_menu, cnf, **kw)

        self.time = 10 #time for entering phrase

    def get_phrases_from_file(self) -> list:
        folder = os.path.dirname(__file__)

        with open(os.path.join(folder, self.file_path), encoding='utf-8') as f:
            phrases = f.read().split('\n')
            phrases = [phrase for phrase in phrases if " - " in phrase]
        return phrases
    
    def cut_phrase(self, phrase) -> (str, str):
        dialog = phrase.split(' - ')
        if len(dialog) > 1:
            part1 = " - ".join(dialog[:-1])
            part2 = dialog[-1]
            return part1, part2
        else:
            return phrase

    def get_tip(self):
        phrase = random.choice(self.learned_phrases)
        display_phrase = self.cut_phrase(phrase)[0]

        self.insert_display_text(text=display_phrase)
    
    def check_entered_phrase(self):
        entered_phrase = self.write_entry.get()

        max_match_percent = 0
        max_match_phrase = ''
        
        for learned in self.learned_phrases:
            right_phrase = self.cut_phrase(phrase=learned)[1]
            match_percent = self.get_strings_match_percent(entered_phrase, right_phrase)
            if match_percent > max_match_percent:
                max_match_percent = match_percent
                max_match_phrase = learned

        if max_match_percent > 80:
            self.phrase_is_right(phrase=max_match_phrase)
            self.get_tip()