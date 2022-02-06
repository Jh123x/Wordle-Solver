class WordNode(object):
    def __init__(self, letter: str, current_dict: dict = None, is_word: bool = False) -> None:
        """A word node within the tree"""
        self.letter: str = letter
        self.dict: dict[str, 'WordNode'] = current_dict if current_dict is not None else {}
        self.is_word: bool = is_word

    def find_template(self, template_string: str) -> list[str]:
        """Find the words based on the template
            only takes into account _ and letters
        """

        if len(template_string) == 0:
            return set([self.letter]) if self.is_word else set()

        current_letter = template_string[0]

        # Wildcard case
        if current_letter == '_':
            results = set()
            for node in self.dict.values():
                results = results.union(node.find_template(template_string[1:]))
        elif current_letter not in self.dict:
            return set()
        else:
            results = self.dict[current_letter].find_template(
                template_string[1:])

        if self.letter is None:
            return results

        return set(map(lambda x: self.letter + x, results))

    def add_word(self, word: str) -> None:
        """Add a word to the Node"""

        # Otherwise create a new node and add it to the dictionary
        letter = word[0]

        if letter not in self.dict:
            new_node = WordNode(letter)
            self.dict[letter] = new_node

        # Recursively add the new node
        node = self.dict[letter]

        if len(word) == 1:
            node.is_word = True
            return

        node.add_word(word[1:])

    def get_all_word(self) -> set[str]:
        """Get all the words in the tree"""
        words = set()
        if self.is_word:
            words.add('')

        for node in self.dict.values():
            curr_all_words = node.get_all_word()
            words = words.union(curr_all_words)
        
        return set(map(lambda x: self.letter + x, words))

    def find_word(self, word: str) -> bool:
        """Find the word given"""
        if len(word) == 0:
            return self.is_word

        letter = word[0]

        # If the letter is not in the dictionary, return False
        if letter not in self.dict:
            return False

        # Recursively find the word
        return self.dict.get(letter).find_word(word[1:])

    def remove(self, word: str) -> bool:
        """Remove a word from the word tree"""

        if len(word) == 0:
            self.is_word = False
            return True

        first_letter = word[0]        
        if first_letter not in self.dict:
            return False
        return self.dict[first_letter].remove(word[1:])

    def __repr__(self) -> str:
        """Return the string representation of the node"""
        return ', '.join(self.get_all_word())
