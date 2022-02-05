import tkinter

from .Settings import Settings


class SettingsScreen(tkinter.Frame):
    def __init__(self, master: tkinter.Tk = None, screen_manager=None, settings: Settings = None, **kwargs) -> None:
        """Settings screen for changing settings"""
        super().__init__(master, **kwargs)
        self.manager = screen_manager
        self.settings = settings
        self.settings_key = {}
        self.settings_offset = 5
        self.generate_widgets()

    def generate_widgets(self) -> None:
        """Generate the widgets for this screen"""
        self._generate_labels()
        self._generate_buttons()
        self._generate_settings()

    def _generate_labels(self) -> None:
        """Generate labels for the settings page"""
        label = tkinter.Label(self, text="Settings", font=('Helvetica', 32))
        label.grid(row=0, column=1, columnspan=9, sticky='n', pady=(0, 20))

    def _generate_buttons(self) -> None:
        """Generate the buttons for the settings page"""
        back_btn = tkinter.Button(
            self,
            text="back",
            command=lambda: self.manager.change_state('menu')
        )
        back_btn.grid(row=0, column=0, pady=(0, 20))

    def save_all_settings(self):
        """Save the settings for all the config"""
        for k, v in self.settings_key.items():
            self.settings.change_settings(k, v.get())

    def _generate_settings(self) -> None:
        """Generate the settings changing screen"""
        for key, value in self.settings.get_settings().items():
            text_var = tkinter.StringVar()
            text_var.set(value)
            self.settings_key[key] = text_var

            label = tkinter.Label(self, text=key)
            entry = tkinter.Entry(self, textvariable=text_var)

            label.grid(
                row=self.settings_offset + len(self.settings_key),
                column=0
            )

            entry.grid(
                row=self.settings_offset + len(self.settings_key),
                column=1,
                columnspan=3
            )
        button = tkinter.Button(
            self,
            text="Save",
            command=self.save_all_settings
        )
        button.grid(
            row=20,
            column=2,
            pady=(10, 10)
        )
