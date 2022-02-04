import tkinter
from os import urandom

from .Settings import Settings
from Guesser.Guesser import Guesser


class GameWindow(tkinter.Frame):
    def __init__(self, master: tkinter.Tk = None, screen_manager=None, settings: Settings = None, **kwargs):
        """The game window for playing the game"""
        super().__init__(master, **kwargs)
        self.screen_manager = screen_manager
        self.settings: Settings = settings
        self.generate_widgets()

        # Wordle related logic
        self.word_list = self._get_word_list()
        self.guesser: Guesser = Guesser(self.word_list)

        # Get the word of the game
        self.word = self.word_list[int(urandom(16).hex(), 16) % len(self.word_list)]
        print(self.word)

    def _get_word_list(self) -> list[str]:
        """Get the word list based on the settings"""
        with open(self.settings.read_settings('wordlist')) as f:
            return list(filter(lambda x: x.strip(), f.readlines()))

    def generate_widgets(self):
        """Generate all the widgets for the screen"""
        self._generate_buttons()
        self._generate_tiles()
        self._generate_labels()

    def _generate_buttons(self):
        """Generate all the buttons for the screen"""
        self.back_btn = tkinter.Button(
            self,
            text="Back",
            command=lambda: self.screen_manager.change_state('menu')
        )
        self.back_btn.grid(row=5, column=5)

    def _generate_tiles(self) -> None:
        """Generate the tiles for showing the wordle word"""
        pass

    def _generate_labels(self):
        """Generate all the labels for the screen"""
        self.title = tkinter.Label(self, text="Wordle", font=("Helvetica", 32))
        self.title.grid(row=0, column=0, columnspan=10, sticky='n')
