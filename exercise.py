import tkinter as tk
import copy
import random


MAX_WIDGET_WIDTH = 75

class Exercise_Frame(tk.Frame):
    name = 'Exercise'
    
    def __init__(self, master, main_menu, cnf={}, **kw):
        tk.Frame.__init__(self, master, cnf, **kw)

        self.main_menu = main_menu
        self.bg = kw['bg']
        self.configure(bg=self.bg)

        #widgets
        self.display_text = None
        self.write_entry = None
        self.learned_count_label = None
        self.unlearned_count_label = None

        self.phrases_backup = self.get_phrases_from_file()
        self.unlearned_phrases = copy.deepcopy(self.phrases_backup)
        self.learned_phrases = []
        self.right_phrases = []

        self.create_widgets()

        self.next_phrase()
    
    def create_widgets(self):
        name_label = tk.Label(self, text=self.__class__.name, font=('Arial 24 bold'), bg=self.bg)
        name_label.pack(fill=tk.X, side=tk.TOP, pady=10)

        #exercise frame
        exercise_frame = tk.Frame(self, bg=self.bg)
        exercise_frame.pack(fill=tk.Y, pady=10)

        self.display_text = tk.Text(exercise_frame, font='Arial 12 bold', bg=self.bg, bd=0, width=MAX_WIDGET_WIDTH, height=3, state='disabled')
        self.display_text.grid(row=0, columnspan=4, sticky='w' + 'e')
        self.display_text.tag_configure("center", justify='center')

        self.write_entry = tk.Entry(exercise_frame, font='Arial 12 bold', bd=0, width=50, justify='center')
        self.write_entry.grid(row=1, columnspan=4, pady=10, sticky='w' + 'e')
        self.write_entry.bind('<Return>', lambda e: self.check_entered_phrase())
        self.write_entry.bind('<Button-3>', lambda e: self.write_entry.delete(0, tk.END))

        next_buton = tk.Button(exercise_frame, text='следующее', font=('Arial 16'), bg='#9cffe0', command=self.next_phrase)
        next_buton.grid(row=2, column=0, sticky='w')

        self.learned_count_label = tk.Label(exercise_frame, bg=self.bg, font='Arial 18 bold')
        self.learned_count_label.grid(row=2, column=1, sticky='w')
        self.unlearned_count_label = tk.Label(exercise_frame, bg=self.bg, font='Arial 18 bold')
        self.unlearned_count_label.grid(row=2, column=2, sticky='e')

        start_training_buton = tk.Button(exercise_frame, text='тренировка', font=('Arial 16'), bg='#9cffe0', command=self.start_training)
        start_training_buton.grid(row=2, column=3, sticky='e')

        self.learned_text = tk.Text(exercise_frame, width=20, height=15, font=('Arial 12'), state='disabled')
        self.learned_text.grid(row=3, columnspan=4, pady=10, sticky='swen')

        menu_button = tk.Button(self, text='главное меню', font=('Arial 16'), bg='#e8e68b', command=self.main_menu.display_main_menu)
        menu_button.pack(side=tk.LEFT, padx=10)

        quit_button = tk.Button(self, text='выход', font=('Arial 16'), bg='#e8e68b', command=self.main_menu.exit)
        quit_button.pack(side=tk.RIGHT, padx=10)
    
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

    def update_counts(self):
        self.unlearned_count_label['text'] = len(self.unlearned_phrases)
        self.learned_count_label['text'] = len(self.learned_phrases)
            
    def insert_display_text(self, text:str):
        self.display_text.config(state='normal')
        self.display_text.delete(1.0, tk.END)
        self.display_text.insert(1.0, text, 'center')
        self.display_text.config(state='disabled')
    
    def insert_learned_text(self, text):
        self.learned_text.config(state='normal')
        self.learned_text.insert(tk.END, text + '\n')
        self.learned_text.config(state='disabled')
    

    def get_full_displayed_phrase(self) -> str:
        displayed_phrase = self.display_text.get(1.0, tk.END).rstrip() #remove '\n'

        for i in range(len(self.learned_phrases)):
            if displayed_phrase in self.learned_phrases[i]:
                return self.learned_phrases[i]
        
        return displayed_phrase

    def phrase_is_right(self, phrase):
        self.write_entry.delete(0, tk.END)
        self.insert_display_text(text='')
        self.insert_learned_text(text=phrase)
        self.learned_phrases.remove(phrase)
        self.right_phrases.append(phrase)
        self.update_counts()    
    
    def next_phrase(self):       
        if len(self.unlearned_phrases) == 0:
            self.start_training()
            return

        phrase = random.choice(self.unlearned_phrases)
        
        self.unlearned_phrases.remove(phrase)
        self.learned_phrases.append(phrase)

        self.insert_display_text(text=phrase)
        self.update_counts()
        self.master.focus()
    
    def check_entered_phrase(self):
        raise NotImplementedError

    def start_training(self):
        raise NotImplementedError
    
    def cut_phrase(self, phrase) -> (str, str):
        raise NotImplementedError

    def get_phrases_from_file(self):
        raise NotImplementedError
    
