import unittest

from bartez.dictionary.trie_node_visitor import *
from bartez.tests.test_utils import *


class TestBartezTrieMatch(unittest.TestCase):

    def test_bartez_trie_visitor_match_word(self):
        dictionary = get_test_trie()
        root = dictionary.get_root()
        match_visitor = BartezDictionaryTrieNodeVisitorMatchWord('zuzzurellone')
        root.accept(match_visitor)
        found = match_visitor.matches()
        print("Word " + match_visitor.get_word() + " found: " + str(found))

    def test_bartez_trie_visitor_word_match_everything(self):
        dictionary = get_test_trie()
        print("Preparing word list")
        list_visitor = BartezDictionaryTrieNodeVisitorList()
        root = dictionary.get_root()
        root.accept(list_visitor)
        words = list_visitor.get_words()
        self.assertTrue(len(words) == 281614)

        print("Matching every word in dictionary ( " + str(len(words)) + " )")
        found = True
        for word in words:
            match_visitor = BartezDictionaryTrieNodeVisitorMatchWord(word)
            root.accept(match_visitor)
            found &= match_visitor.matches()
        print("Found every word in dictionary: " + str(found))

    def test_bartez_trie_visitor_match_word_not_present(self):
        dictionary = get_test_trie()
        root = dictionary.get_root()
        match_visitor = BartezDictionaryTrieNodeVisitorMatchWord('networkx')
        root.accept(match_visitor)
        found = match_visitor.matches()
        print("Word " + match_visitor.get_word() + " found: " + str(found))
        self.assertFalse(found)


if __name__ == '__main__':
    unittest.main()
