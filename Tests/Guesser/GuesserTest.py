import unittest

from Guesser.Guesser import HardcoreGuesser

wordlist_file = 'wordle-answers-alphabetical.txt'
with open(wordlist_file) as f:
    wordlist = f.readlines()


class GuesserTest(unittest.TestCase):
    def setUp(self) -> None:
        self.guesser = HardcoreGuesser(wordlist)
        self.less_guesser = HardcoreGuesser(['slate', 'plate'])
        self.blank_guesser = HardcoreGuesser([])
        return super().setUp()

    def test_2nd_letter_not_found(self):
        self.guesser.get_best_guess('____s', 'sssss', self.guesser.contains)
        self.assertEqual(self.guesser.contains, {'s': 1})
        self.assertTrue(self.guesser.is_valid_word('fleas'))

    def test_is_valid_word_success(self):
        self.assertTrue(self.guesser.is_valid_word('slate'))
        self.assertTrue(self.guesser.is_valid_word('clote'))

    def test_is_valid_word_failure(self):
        word = 'slate'
        valid_word = 'plate'
        self.guesser.get_best_guess('_late', word)
        self.assertFalse(self.guesser.is_valid_word(word))
        self.assertTrue(self.guesser.is_valid_word(valid_word))

        self.less_guesser.get_best_guess('_late', word)
        self.assertFalse(self.less_guesser.is_valid_word(word))
        self.assertTrue(self.less_guesser.is_valid_word(valid_word))

    def test_to_tree_template(self):
        normal_template = '______'
        self.assertEqual(self.guesser.to_tree_template_string(
            normal_template), normal_template)

        normal_template2 = 'abcd__'
        self.assertEqual(self.guesser.to_tree_template_string(
            normal_template2), normal_template2)

        converted_template = 'ABCD__'
        self.assertEqual(self.guesser.to_tree_template_string(
            converted_template), normal_template)

        test_template = '_l_TE'
        result = '_l___'
        self.assertEqual(self.guesser.to_tree_template_string(test_template), result)

    def test_to_contains_dict(self):
        contains_dict = {
            's': 2,
            'l': 2,
            'a': 1,
        }
        word = 'slals'
        self.assertEqual(self.guesser.to_contains_dict(word), contains_dict)

        contains_dict2 = {
            's': 1,
            'l': 1,
            'a': 1,
            't': 1,
            'e': 1,
        }
        word2 = 'slate'
        self.assertEqual(self.guesser.to_contains_dict(word2), contains_dict2)

    def test_process_template_string(self):
        template_string = 'AbcD__'
        previous_guess = 'abcdee'
        self.guesser.process_template_string(template_string, previous_guess)
        self.assertEqual(self.guesser.contains, {'a': 1, 'b': 1, 'c': 1, 'd': 1})
        self.assertEqual(self.guesser.wrong_list, {(0, 'a'), (3, 'd')})
        self.assertEqual(self.guesser.all_wrong_list, {'e'})
