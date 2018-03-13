import unittest

from bartez.dictionary.trie import BartezDictionaryTrie
from bartez.dictionary.trie_node_visitor import *
from bartez.dictionary.trie_serializer import *
from bartez.tests.test_utils import *

test_trie = None
test_trie_small = None

class TestBartezTrie(unittest.TestCase):
    def test_bartez_trie_creation(self):
        global test_trie
        test_trie = BartezDictionaryTrie('italian', get_test_dictionary_path())

        global test_trie_small
        test_trie_small = BartezDictionaryTrie('italian', get_test_dictionary_path_1000())

        self.assertTrue(test_trie.is_loaded() is True)

    def test_bartez_trie_visitor_list(self):
        global test_trie_small
        list_visitor = BartezDictionaryTrieNodeVisitorList()
        root = test_trie_small.get_root()
        root.accept(list_visitor)
        words = list_visitor.get_words()
        self.assertTrue(len(words) == 1000)

    def test_bartez_trie_visitor_list_long(self):
        global test_trie
        list_visitor = BartezDictionaryTrieNodeVisitorList()
        root = test_trie.get_root()
        root.accept(list_visitor)
        words = list_visitor.get_words()
        self.assertTrue(len(words) == 281614)

    def test_bartez_trie_visitor_count(self):
        global test_trie
        counter_visitor = BartezDictionaryTrieNodeVisitorNodeCounter()
        root = test_trie.get_root()
        root.accept(counter_visitor)
        terminal_count = counter_visitor.get_terminal_count()
        non_terminal_count = counter_visitor.get_non_terminal_count()
        nodes_count = counter_visitor.get_nodes_count()
        print("Nodes: " + str(nodes_count) + "\n" +
              "Terminal Nodes: " + str(terminal_count) + "\n" +
              "Non Terminal Nodes: " + str(non_terminal_count) + "\n")

    def test_bartez_trie_visitor_word_match(self):
        global test_trie
        root = test_trie.get_root()
        match_visitor = BartezDictionaryTrieNodeVisitorWordMatch('zuzzurellone')
        root.accept(match_visitor)
        found = match_visitor.matches()
        print("Word " + match_visitor.get_word() + " found: " + str(found))

    def test_bartez_trie_visitor_word_match_everything(self):
        global test_trie
        print("Preparing word list")
        list_visitor = BartezDictionaryTrieNodeVisitorList()
        root = test_trie.get_root()
        root.accept(list_visitor)
        words = list_visitor.get_words()
        self.assertTrue(len(words) == 281614)

        print("Matching every word in dictionary")
        found = True
        for word in words:
            match_visitor = BartezDictionaryTrieNodeVisitorWordMatch(word)
            root.accept(match_visitor)
            found &= match_visitor.matches()

        print("Found every word in dictionary: " + str(found))

    def test_bartez_trie_visitor_word_not_match(self):
        global test_trie
        root = test_trie.get_root()
        match_visitor = BartezDictionaryTrieNodeVisitorWordMatch('networkx')
        root.accept(match_visitor)
        found = match_visitor.matches()
        print("Word " + match_visitor.get_word() + " found: " + str(found))
        self.assertFalse(found)

    def test_bartez_trie_serialize(self):
        global test_trie
        bartez_trie_save_to_file(test_trie, "bartez_trie.btt")
        trie_loaded = bartez_trie_load_from_file("bartez_trie.btt")
        self.assertTrue(trie_loaded is not None)


if __name__ == '__main__':
    unittest.main()
