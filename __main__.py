import argparse
import tkinter

from GUI.ScreenManager import ScreenManager
from Guesser.Guesser import HardcoreGuesser


def read_word_list(filename: str) -> list[str]:
    with open(filename, 'r') as f:
        data = f.readlines()
    return [word.strip().lower() for word in data]


def play_cli(wordlist: list[str]) -> None:
    # Create word tree
    guesser = HardcoreGuesser(wordlist)

    # 5 tries total
    recommended_guess = guesser.default_guess
    guess = None
    guesses = 0
    chances = 1 / len(word_list)
    while True:
        print("Small letter for correct position and letter")
        print("Capital letter for correct letter wrong position")
        print("'_' for wrong letter not in word")
        print("'q' to quit anytime")
        print(f"Recommended Guess: {recommended_guess}. Chances {chances}")
        guess = None
        result = None

        while guess is None or len(result) != len(guess):
            if guess is not None:
                print(
                    f"Result ({result}) is different length from guess ({guess})")
            guess = input("Guess Tried [Leave blank if recommeded guess]: ")
            if guess == 'q':
                return

            if len(guess) == 0:
                guess = recommended_guess

            result = input("Enter the results: ")
            if result == 'q':
                break

        recommended_guess, chances = guesser.get_best_guess(result, guess)
        guesses += 1

        if result == recommended_guess:
            break

    print(f"Total guesses: {guesses}\nWord: {result}")


def play_gui() -> None:
    """Play the game with a GUI"""
    root = tkinter.Tk()
    manager = ScreenManager(root)
    root.mainloop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Wordle Solver')
    parser.add_argument('-w', '--wordlist',
                        help='Wordlist to use')
    parser.add_argument('-g', '--gui', help='Run the GUI', action='store_true')

    args = parser.parse_args()

    if args.gui:
        play_gui()
    else:
        word_list = read_word_list(args.wordlist)
        play_cli(word_list)
