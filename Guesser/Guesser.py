from pprint import pprint
from Tree import WordTree


class Guesser(object):
    def __init__(self, word_list: list[str]) -> None:
        """A list to sort frquencies of the words in question"""
        self.word_tree = WordTree(word_list)
        # Find the max freqency of letter at that position.
        letters = [{} for _ in range(5)]
        for word in word_list:
            for index, letter in enumerate(word):
                letters[index][letter] = letters[index].get(letter, 0) + 1
        self.letters = letters
        self.wrong_list = []
        self.all_wrong_list = []

    # Function to calculate the score of the word
    def _score_calc(self, word: str) -> int:
        score = 0
        for index, letter in enumerate(word):
            score += self.letters[index].get(letter, 0)
        return score

    def get_best_guess(self, template_string: str, previous_guess: str) -> str:
        """Get the best guess"""
        # Get caps string
        for index, letter in enumerate(template_string):
            if letter.isupper():
                self.wrong_position_list.append((index, letter))
            if letter == '_':
                self.all_wrong_list.append(previous_guess[index])
        words = self.word_tree.find_template(template_string)
        new_words = []
        for word in words:
            is_wrong = False
            for letter in self.all_wrong_list:
                if letter in word:
                    is_wrong = True
            if is_wrong:
                continue
            for index, letter in self.wrong_list:
                if word[index] == letter:
                    is_wrong = True
                    break
            if is_wrong:
                continue
            new_words.append(word)
        return max(new_words, key=self._score_calc)
