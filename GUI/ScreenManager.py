import tkinter

from .SettingsScreen import SettingsScreen
from .Menu import Menu
from .Game import GameWindow
from .Settings import Settings


class ScreenManager(object):

    # Store the possible frams
    screen_states: dict[str, tkinter.Frame] = {
        'menu': Menu,
        'game': GameWindow,
        'settings': SettingsScreen,
    }

    def __init__(self, master: tkinter.Tk, start_state: str = 'menu', default_setting_path: str = 'settings.cfg') -> None:
        """A screen manager for managing what is the current screen"""
        self.master: tkinter.Tk = master
        self.current_screen = None
        self.settings = Settings(default_setting_path)
        self.master.title(self.settings.read_settings('title'))
        self.master.geometry(self.settings.read_settings('geometry'))
        self.change_state(start_state)

    def transition(self) -> None:
        """Transition to the next screen"""
        if self.current_screen is not None:
            self._unload_screen()
        self.current_screen = self.screen_states[self.current](
            self.master, self, settings=self.settings)
        self._load_screen()

    def change_state(self, new_state: str) -> None:
        """Change the current state"""
        self.current = new_state
        self.transition()

    def _unload_screen(self) -> None:
        """Unload the screen based on current screen"""
        self.current_screen.place_forget()

    def _load_screen(self) -> None:
        """Load the screen based on current state"""
        self.current_screen.place(relx=.5, rely=.5, anchor='center')
