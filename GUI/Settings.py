import configparser
import os


class Settings(object):
    def __init__(self, settings_file: str):
        """Settings for the GUI"""
        self.settings_path: str = settings_file
        self.changed: bool = False

        # If settings does not exists, generate a default settings file
        if not os.path.exists(settings_file):
            self.generate_default_config(settings_file)

        self.parser: configparser.RawConfigParser = configparser.RawConfigParser()
        self.parser.read(settings_file)

    def generate_default_config(self, filename: str) -> None:
        """Generate a default config based on the filename"""
        parser = configparser.RawConfigParser()
        parser.add_section('SETTINGS')
        parser.set('SETTINGS', '; The wordlist to use for the program')
        parser.set('SETTINGS', 'wordlist', 'wordle-answers-alphabetical.txt')
        parser.set('SETTINGS', '; The title of the window')
        parser.set('SETTINGS', 'title', "Wordle")
        parser.set('SETTINGS', '; Geometry of the window')
        parser.set('SETTINGS', 'geometry', "800x600")
        parser.set('SETTINGS', 'guesses', "6")
        with open(filename, 'w') as configfile:
            parser.write(configfile)

    def get_settings(self) -> dict:
        """Get all the settings"""
        return self.parser['SETTINGS']

    def read_settings(self, key: str) -> str:
        """Read the settings"""
        return self.parser['SETTINGS'][key]

    def change_settings(self, key: str, value: str) -> bool:
        """Change the settings"""
        if key not in self.parser['SETTINGS']:
            return False
        self.parser.set('SETTINGS', key, value)
        self.changed = True
        return True

    def __del__(self) -> None:
        """Save the settings"""
        if not self.changed:
            return
        with open(self.settings_path, 'w') as configfile:
            self.parser.write(configfile)
