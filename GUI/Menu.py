import tkinter

from .Settings import Settings


class Menu(tkinter.Frame):
    def __init__(self, master: tkinter.Tk = None, screen_manager=None, settings: Settings = None, **kwargs):
        """The menu screen for Wordle."""
        assert settings is not None

        super().__init__(master, **kwargs)
        self.manager = screen_manager
        self.generate_widgets()

    def generate_widgets(self) -> None:
        """Generate all the widgets for the screen."""
        self._generate_labels()
        self._generate_buttons()

    def _generate_labels(self) -> None:
        """Generate all the labels for the widget."""
        self.title_label = tkinter.Label(
            self, text="Wordle", font=("Helvetica", 64))
        self.title_label.grid(row=0, column=0, columnspan=10,
                              sticky='nesw', pady=(0, 30))

    def _generate_buttons(self) -> None:
        """Generate all the buttons for the widget."""
        button_space = (0, 5)
        play_button = tkinter.Button(
            self,
            text="Play",
            command=lambda: self.manager.change_state('game')
        )
        play_button.grid(row=5, column=5, pady=button_space)

        settings_button = tkinter.Button(
            self,
            text="Settings",
            command=lambda: self.manager.change_state('settings')
        )
        settings_button.grid(row=6, column=5, pady=button_space)
