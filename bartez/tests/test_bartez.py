import unittest

from bartez.tests.test_utils import *
from bartez.word_dictionary import Dictionary


class TestBartez(unittest.TestCase):
    def test_bartez_dictionary(self):
        dictionary = get_test_dictionary()
        self.assertTrue(dictionary.get_page_count() > 0)
        self.assertTrue(dictionary.get_words_count() > 0)
        self.assertTrue(len(dictionary.get_language()) > 0)

    def test_bartez_dictionary(self):
        dictionary = get_test_dictionary_1000()
        self.assertTrue(dictionary.get_page_count() > 0)
        self.assertTrue(dictionary.get_words_count() > 0)
        self.assertTrue(len(dictionary.get_language()) > 0)

if __name__ == '__main__':
    unittest.main()
