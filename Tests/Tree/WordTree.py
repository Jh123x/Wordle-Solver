from unittest import TestCase

from Tree.WordTree import WordTree


class WordTreeTest(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.a_tree = WordTree(['a'])
        self.b_tree = WordTree([])
        self.tree = WordTree(['hello', 'world', 'bye'])
        self.hello_tree = WordTree(['hello'])
        self.h_list = ['hello', 'hi', 'hee', 'hitler']
        self.h_tree = WordTree(self.h_list)
        self.w_list = ['plate', 'slate']
        self.w_tree = WordTree(self.w_list)

    def test_find_template_string_wildcard(self):
        self.assertEqual(self.h_tree.find_template("______"), set(['hitler']))
        self.assertEqual(self.tree.find_template('_____'), {'hello', 'world'})
        self.assertEqual(self.b_tree.find_template("_"), set())
        self.assertEqual(self.a_tree.find_template("_"), set(['a']))
        self.assertEqual(self.h_tree.find_template("___"), set(['hee']))
        self.assertEqual(self.h_tree.find_template("hi____"), set(['hitler']))
        self.assertEqual(self.w_tree.find_template('_late'), set(self.w_list))

    def test_find_template_string_no_wildcard(self):
        self.assertEqual(self.w_tree.find_template('plate'), set(['plate']))

    def test_find_template_string_with_caps(self):
        self.assertEqual(self.w_tree.find_template('PLATE'), set(['plate']))

    def test_get_all(self):
        self.assertEqual(self.h_tree.get_all_word(), set(self.h_list))
        self.assertEqual(self.a_tree.get_all_word(), set(['a']))
        self.assertEqual(self.b_tree.get_all_word(), set())
        self.assertEqual(self.w_tree.get_all_word(), set(self.w_list))

    def test_word_is_really_added(self):
        curr = self.hello_tree.root
        self.assertTrue('h' in curr)
        curr = curr.get('h').dict
        self.assertEqual(1, len(curr))
        self.assertTrue('e' in curr)
        curr = curr.get('e').dict
        self.assertEqual(1, len(curr))
        self.assertTrue('l' in curr)
        curr = curr.get('l').dict
        self.assertEqual(1, len(curr))
        self.assertTrue('l' in curr)
        curr = curr.get('l').dict
        self.assertEqual(1, len(curr))
        self.assertTrue('o' in curr)
        curr = curr.get('o')
        self.assertEqual(0, len(curr.dict))
        self.assertTrue(curr.is_word)

    def test_is_word_true(self):
        """Test if 'a' is a word"""
        self.assertTrue(self.a_tree.find('a'))

    def test_is_word_false(self):
        """Test if 'b' is a word"""
        self.assertFalse(self.b_tree.find('b'))
        self.assertFalse(self.a_tree.find('b'))
        self.assertFalse(self.tree.find('hollo'), self.tree)

    def test_find_word_equal_current_letter(self):
        """Test if words can be found in tree"""
        self.assertTrue(self.a_tree.find('a'))
        self.assertTrue(self.tree.find('world'))
        self.assertTrue(self.tree.find('bye'))
        self.assertTrue(self.tree.find('hello'))

    def test_unable_to_find_word(self):
        """Test if a non-existent word can be found"""
        self.assertFalse(self.b_tree.find('a'))
        self.assertFalse(self.tree.find('a'))

    def test_remove_word_from_empty_tree(self):
        """Test if a word is correctly removed from an empty tree"""
        self.assertFalse(self.b_tree.remove('b'), f"Tree: {self.b_tree}")

    def test_remove_word_from_tree_with_1_element(self):
        """Test if a word is correctly removed from tree with 1 element"""
        self.assertTrue(self.a_tree.find('a'), f"Tree: {self.a_tree}")
        self.assertTrue(self.a_tree.remove('a'), f"Tree: {self.a_tree}")
        self.assertFalse(self.a_tree.find('a'))

    def test_remove_word_from_tree_with_multiple_elements(self):
        """Test if a word with multiple elements is removed correctly"""
        for index, word in enumerate(self.h_list):
            self.assertTrue(
                self.h_tree.find(word),
                f"Tree: {self.h_tree}. Finding: {word}"
            )
            self.assertTrue(
                self.h_tree.remove(word),
                f"Tree: {self.h_tree}. Removing: {word}"
            )
            self.assertFalse(
                self.h_tree.find(word),
                f"Tree: {self.h_tree}. Finding after removed: {word}"
            )
            for word in self.h_list[index+1:]:
                self.assertTrue(
                    self.h_tree.find(word),
                    f"Tree: {self.h_tree}. Finding remaining words after removed: {word}"
                )

    def test_get_all_words(self):
        """Test if all words are returned"""
        self.assertEqual(
            self.h_tree.get_all_word(),
            set(self.h_list)
        )

        self.assertTrue(self.h_tree.remove('hello'))

        expected = self.h_list.copy()
        expected.remove('hello')

        self.assertEqual(
            self.h_tree.get_all_word(),
            set(expected)
        )
