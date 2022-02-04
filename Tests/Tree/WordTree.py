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
        
    def test_find_template_string_wildcard(self):
        self.assertEqual(self.b_tree.find_template("_"), set())
        self.assertEqual(self.a_tree.find_template("_"), set(['a']))
        self.assertEqual(self.h_tree.find_template("___"), set(['hee']))
        self.assertEqual(self.h_tree.find_template("hi____"), set(['hitler']))

    def test_get_all(self):
        self.assertEqual(self.h_tree.get_all_word(), set(self.h_list))
        self.assertEqual(self.a_tree.get_all_word(), set(['a']))
        self.assertEqual(self.b_tree.get_all_word(), set())

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

