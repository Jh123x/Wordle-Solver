from .WordNode import WordNode


class WordTree(object):
    def __init__(self, word_list: list[str]) -> None:
        """A word tree that efficiently stores and searches words"""
        self.root: dict[WordNode] = {}
        self._build_tree(word_list)

    def _build_tree(self, word_list: list[str]):
        """Build a tree based on the word list"""
        for word in word_list:
            first_letter = word[0]
            node = self.root.get(first_letter, WordNode(first_letter))
            self.root[first_letter] = node

            if len(word) == 1:
                node.is_word = True
            else:
                remaining_word = word[1:]
                node.add_word(remaining_word)

    def get_all_word(self) -> set[str]:
        results = set()
        for node in self.root.values():
            results = results.union(node.get_all_word())
        return results

    def find_template(self, template_string: str) -> list[str]:
        """Find a list of words based on the template provided
            Only takes into account _ and letters
        """
        first_letter = template_string[0]
        if first_letter == '_':
            results = set()
            for node in self.root.values():
                results = results.union(node.find_template(template_string[1:]))
            return results
        if first_letter in self.root:
            return self.root.get(first_letter).find_template(template_string[1:])

        if first_letter.lower() in self.root:
            results = set()
            for node in self.root.values():
                results.union(node.find_template(template_string[1:]))
            return set(filter(lambda x: not x.startswith(first_letter), results))

        return set()

    def find(self, word: str) -> bool:
        """Find the word in the tree"""
        if len(word) == 1:
            return word in self.root and self.root[word].is_word

        first_letter = word[0]
        return first_letter in self.root and self.root[first_letter].find_word(word[1:])

    def __repr__(self) -> str:
        return self.root.__repr__()
