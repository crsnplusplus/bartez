import unittest

from bartez.dictionary.trie_node_visitor import *
from bartez.tests.test_utils import *


class TestBartezTrie(unittest.TestCase):

    def test_bartez_trie_creation(self):
        dictionary = get_test_trie()
        dictionary_small = get_test_trie_small()
        self.assertTrue(dictionary.is_loaded() is True)
        self.assertTrue(dictionary_small.is_loaded() is True)

    def test_bartez_trie_visitor_list(self):
        dictionary_small = get_test_trie_small()
        list_visitor = BartezDictionaryTrieNodeVisitorList()
        root = dictionary_small.get_root()
        root.accept(list_visitor)
        words = list_visitor.get_words()
        print("found " + str(len(words)) + " words")
        self.assertTrue(len(words) == 1000)

    def test_bartez_trie_visitor_list_long(self):
        dictionary = get_test_trie()
        list_visitor = BartezDictionaryTrieNodeVisitorList()
        root = dictionary.get_root()
        root.accept(list_visitor)
        words = list_visitor.get_words()
        self.assertTrue(len(words) == 281614)

    def test_bartez_trie_visitor_count(self):
        dictionary = get_test_trie()
        counter_visitor = BartezDictionaryTrieNodeVisitorNodeCounter()
        root = dictionary.get_root()
        root.accept(counter_visitor)
        terminal_count = counter_visitor.get_terminal_count()
        non_terminal_count = counter_visitor.get_non_terminal_count()
        nodes_count = counter_visitor.get_nodes_count()
        print("Nodes: " + str(nodes_count) + "\n" +
              "Terminal Nodes: " + str(terminal_count) + "\n" +
              "Non Terminal Nodes: " + str(non_terminal_count) + "\n")

if __name__ == '__main__':
    unittest.main()
