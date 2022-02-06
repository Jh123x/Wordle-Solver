from math import log2
from typing import Iterable
from Tree import WordTree
from itertools import permutations


class HardcoreGuesser(object):
    result_function = (lambda x: "_", lambda x: x.upper(), lambda x: x.lower())

    def __init__(self, word_list: list[str], word_length: int = -1) -> None:
        """A list to sort frquencies of the words in question"""
        # Find the max freqency of letter at that position.
        if word_length == -1:
            word_length = len(word_list[0].strip())

        # String whitespaces
        self.word_list:set = set(word.strip() for word in word_list)
        self.word_tree = WordTree(word_list)

        self.letters = [{} for _ in range(word_length)]
        self.letter_freq = {}
        for word in self.word_list:
            for index, letter in enumerate(word):
                self.letters[index][letter] = self.letters[index].get(letter, 0) + 1
                self.letter_freq[letter] = self.letter_freq.get(letter, 0) + 1

        self.letters_max = list(map(lambda x: max(x.values()), self.letters))
        self.letter_freq_max = max(self.letter_freq.values())

        # Get the default guess based on the wordlist
        self.default_guess = max(self.word_list, key=self._score_calc)

        self.wrong_list = set()
        self.contains = {}
        self.max_contain = {}
        self.all_wrong_list = set()

    def reset(self):
        """Reset the state of the guesser"""
        self.wrong_list = set()
        self.max_contain = {}
        self.all_wrong_list = set()

    def _get_permutations(self, word:str) -> Iterable[str]:
        """Get the possible permuatations of the word of length"""
        possible_results = permutations(self.result_function, len(word))
        for functions in possible_results:
            template_word = []
            for index, f in enumerate(functions):
                template_word.append(f(word[index]))
            yield ''.join(template_word)

    # Function to calculate the score of the word
    def _score_calc(self, word: str) -> int:
        """Calculate the score of the word"""
        score = 0
        all_words = self.word_tree.get_all_word()
        for possible_result in self._get_permutations(word):
            word_list = tuple(filter(self._is_valid_word, self.word_tree.find_template(possible_result)))
            px = len(word_list)/ all_words
            score += log2(px) * 1 / len(px)
        return score

    def is_valid_word(self, word: str) -> bool:
        """Check if the string can be part of the word given current information"""

        contain_dict = self.to_contains_dict(word)

        for k,v in self.max_contain.items():
            if k not in contain_dict or contain_dict[k] >= v:
                return False

        for index, letter in self.wrong_list:
            if word[index] == letter:
                return False

        for letter in self.all_wrong_list:
            if letter in word:
                return False

        return True

    def is_word(self, word:str) -> bool:
        """Check if the current word is a word"""
        return word in self.word_list

    def to_tree_template_string(self, template_string: str) -> str:
        """Convert the original template string to a tree template string"""
        acc = []
        for letter in template_string:
            if letter.isupper():
                acc.append('_')
            else:
                acc.append(letter)
        return ''.join(acc)

    def to_contains_dict(self, template_string: str) -> dict[str, int]:
        """Convert a template string to a dict"""
        d = {}
        for letter in template_string:
            if letter == '_':
                continue
            d[letter.lower()] = d.get(letter.lower(), 0) + 1
        return d

    def process_template_string(self, template_string: str, previous_guess: str) -> None:
        """Process the previous template string"""
        to_be_all_wrong = set()
        for index, letter in enumerate(template_string):

            # Upper case add the index wrongs.
            if letter.isupper():
                lower_letter = letter.lower()
                self.wrong_list.add((index, lower_letter))

            # Wildcard means it does not exists in the word.
            elif letter == '_':
                to_be_all_wrong.add(previous_guess[index])

        # Convert word to dict and update the current contains
        self.contains = self.to_contains_dict(template_string)

        for letter in to_be_all_wrong:
            if letter not in self.contains:
                self.all_wrong_list.add(letter)
                continue
            self.max_contain[letter] = self.contains[letter] + 1

    def get_best_guess(self, template_string: str, previous_guess: str = None) -> tuple[str, float]:
        """Get the best guess"""

        # Get caps string
        self.process_template_string(template_string, previous_guess)
        temp_template_string = self.to_tree_template_string(template_string)

        words = self.word_tree.find_template(temp_template_string)

        if len(words) == 0:
            raise ValueError(f"No words found for template string '{temp_template_string}'.")

        if len(words) == 1:
            return tuple(words)[0], 1

        for word in words:
            if not self.is_valid_word(word):
                self.word_tree.remove(word)
                continue
        new_words = self.word_tree.get_all_word()

        return max(new_words, key=self._score_calc), 1/len(new_words)
