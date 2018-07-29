import unittest

from bartez.dictionary.trie import *
from bartez.dictionary.trie_node import *
from bartez.dictionary.trie_node_visitor import *
from bartez.tests.test_utils import *

class Test_bartez_trie(unittest.TestCase):
    def test_bartez_trie_creation(self):
        trie = BartezTrie('italian', 'words_test_1000.txt')
        self.assertTrue(trie.is_loaded() is True)


    def test_bartez_trie_visitor_print(self):
        trie = BartezTrie('italian', 'words_test_1000.txt')
        printVisitor = BartezNodeVisitorPrint()
        root = trie.get_root()
        root.accept(printVisitor)
        self.assertTrue(trie.is_loaded() is True)


    def test_bartez_trie_visitor_list(self):
        trie = BartezTrie('italian', 'words_test_1000.txt')
        listVisitor = BartezNodeVisitorList()
        root = trie.get_root()
        root.accept(listVisitor)
        words = listVisitor.get_words()
        len_words = len(words)
        print("words_count " +  str(len(words)))
        self.assertTrue(len(words) is 3001)


    def test_bartez_trie_visitor_list_long(self):
        trie = BartezTrie('italian', 'words.txt')
        listVisitor = BartezNodeVisitorList()
        root = trie.get_root()
        root.accept(listVisitor)
        words = listVisitor.get_words()
        len_words = len(words)
        self.assertTrue(len(words) is 281614)

if __name__ == '__main__':
    unittest.main()
