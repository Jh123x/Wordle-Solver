import tkinter
from os import urandom
from turtle import width

from .Settings import Settings
from Guesser.Guesser import Guesser


class GameWindow(tkinter.Frame):
    def __init__(self, master: tkinter.Tk = None, screen_manager=None, settings: Settings = None, **kwargs):
        """The game window for playing the game"""
        super().__init__(master, **kwargs)
        self.screen_manager = screen_manager
        self.settings: Settings = settings
        self.tile_list = []
        self.tile_list_sv = []

        # Wordle related logic
        self.word_list = self._get_word_list()
        self.guesser: Guesser = Guesser(self.word_list)
        self.current_word = 0
        self.word_len = len(self.guesser.default_guess)

        # Get the word of the game
        self.word = self.word_list[int(
            urandom(16).hex(), 16) % len(self.word_list)].strip()
        self.generate_widgets()

    def _get_word_list(self) -> list[str]:
        """Get the word list based on the settings"""
        with open(self.settings.read_settings('wordlist')) as f:
            return list(filter(lambda x: x.strip(), f.readlines()))

    def generate_widgets(self):
        """Generate all the widgets for the screen"""
        self._generate_buttons()
        self._generate_tiles()
        self._generate_labels()
        self._generate_text_box()

    def win(self):
        """The win screen"""
        tkinter.messagebox.showinfo(
            "You win!", f"You win! The word was{self.word}")
        self.screen_manager.change_state('menu')

    def _submit_word(self) -> None:
        word = self.text_box.get().strip()
        if len(word) != self.word_len:
            tkinter.messagebox.showerror(
                'Error', f'Word must be {self.word_len} letters long')
            return

        if not self.guesser.is_word(word):
            tkinter.messagebox.showerror(
                'Error', f'{word} is not a valid word')
            return

        current_word = self.current_word
        self.text_box.delete(0, 'end')
        self.current_word += 1
        contains_dict = self.guesser.to_contains_dict(self.word)

        # Update the labels
        for index in range(current_word*self.word_len, (current_word+1)*self.word_len):
            i = index-current_word*self.word_len
            current_letter = word[i]
            correct_letter = self.word[i]
            var = self.tile_list_sv[index]
            var.set(current_letter)
            label = self.tile_list[index]

            # Remove label
            label.grid_forget()

            # Update with new color
            if current_letter == correct_letter:
                label.config(bg="green")
                contains_dict[correct_letter] -= 1
            else:
                label.config(bg="grey")

        for index in range(current_word*self.word_len, (current_word+1)*self.word_len):
            current_letter = word[index-current_word*self.word_len]
            label = self.tile_list[index]
            if current_letter in contains_dict and contains_dict[current_letter] > 0:
                label.config(bg="yellow")
                contains_dict[current_letter] -= 1
            label.grid(row=index//self.word_len+2, column=index %
                       self.word_len, sticky='nsew', padx=(10, 10), pady=(10, 10))

        print(word.lower(), self.word.lower(), word.lower() == self.word.lower())
        if word.lower() == self.word.lower():
            return self.win()

    def _generate_buttons(self):
        """Generate all the buttons for the screen"""
        self.back_btn = tkinter.Button(
            self,
            text="Back",
            command=lambda: self.screen_manager.change_state('menu')
        )
        self.back_btn.grid(row=0, column=0)

        self.submit_btn = tkinter.Button(
            self,
            text="Submit",
            command=self._submit_word
        )
        self.submit_btn.grid(row=20, column=10, sticky='s')

    def _generate_text_box(self):
        """Generate textbox to be used"""
        self.text_box = tkinter.Entry(self, font=("Helvetica", 32))
        self.text_box.grid(row=20, column=0, columnspan=8, sticky='s')

    def _generate_tiles(self) -> None:
        """Generate the tiles for showing the wordle word"""

        for y in range(6):
            for x in range(self.word_len):
                var = tkinter.StringVar()
                var.set(" ")
                tile = tkinter.Label(self, textvariable=var, font=(
                    "Helvetica", 32), bg="white")
                tile.grid(
                    row=y+2,
                    column=x,
                    sticky='nsew',
                    padx=(10, 10), pady=(10, 10)
                )
                self.tile_list.append(tile)
                self.tile_list_sv.append(var)

    def _generate_labels(self):
        """Generate all the labels for the screen"""
        self.title = tkinter.Label(self, text="Wordle", font=("Helvetica", 32))
        self.title.grid(row=0, column=1, columnspan=9, sticky='n')
