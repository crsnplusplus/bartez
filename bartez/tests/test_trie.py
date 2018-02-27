import unittest

from bartez.dictionary.trie import *
from bartez.dictionary.trie_node_visitor import *
from bartez.tests.test_utils import *


class TestBartezTrie(unittest.TestCase):
    def test_bartez_trie_creation(self):
        trie = BartezTrie('italian', get_test_dictionary_path())
        self.assertTrue(trie.is_loaded() is True)

    def test_bartez_trie_visitor_print(self):
        trie = BartezTrie('italian', get_test_dictionary_path_1000())
        print_visitor = BartezNodeVisitorPrint()
        root = trie.get_root()
        root.accept(print_visitor)
        self.assertTrue(trie.is_loaded() is True)

    def test_bartez_trie_visitor_list(self):
        trie = BartezTrie('italian', get_test_dictionary_path_1000())
        list_visitor = BartezNodeVisitorList()
        root = trie.get_root()
        root.accept(list_visitor)
        words = list_visitor.get_words()
        self.assertTrue(len(words) == 1000)

    def test_bartez_trie_visitor_list_long(self):
        trie = BartezTrie('italian', get_test_dictionary_path())
        list_visitor = BartezNodeVisitorList()
        root = trie.get_root()
        root.accept(list_visitor)
        words = list_visitor.get_words()
        self.assertTrue(len(words) == 281614)


if __name__ == '__main__':
    unittest.main()
