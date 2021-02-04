import tkinter as tk
from tkinter import filedialog
from importlib import reload
import random
import os
from datetime import datetime

import exercise
reload(exercise)


class Exercise(exercise.Exercise_Frame):
    name = 'Фразы'

    def __init__(self, master, main_menu, cnf={}, **kw):
        self.file_path = filedialog.askopenfilename(initialdir=os.path.dirname(__file__),
                                                title="Select file", filetypes=(("txt files", "*.txt"), ))
                                                
        exercise.Exercise_Frame.__init__(self, master, main_menu, cnf, **kw)

        self.time = 10 #time for entering phrase

    def get_phrases_from_file(self) -> list:
        folder = os.path.dirname(__file__)

        with open(os.path.join(folder, self.file_path), encoding='utf-8') as f:
            phrases = f.read().split('\n')
            phrases = [phrase for phrase in phrases if " - " not in phrase]
        return phrases
    
    def check_entered_phrase(self):
        entered_phrase = self.write_entry.get()

        max_match_percent = 0
        max_match_phrase = ''
        
        for learned in self.learned_phrases:
            match_percent = self.get_strings_match_percent(entered_phrase, learned)
            if match_percent > max_match_percent:
                max_match_percent = match_percent
                max_match_phrase = learned

        if max_match_percent > 80:
            self.phrase_is_right(phrase=max_match_phrase)
    
    def cut_phrase(self, phrase) -> (str, str):
        phrase = phrase.split(' ')
        part1 = ' '.join(phrase[len(phrase)//2:])
        part2 = ' '.join(phrase[:len(phrase)//2])
        return part1, part2