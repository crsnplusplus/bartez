import unittest

from bartez.dictionary.trie import BartezDictionaryTrie
from bartez.dictionary.trie_node_visitor import *
from bartez.dictionary.trie_serializer import *
from bartez.tests.test_utils import *

test_trie = None
test_trie_small = None

def get_test_trie():
    global test_trie
    if test_trie is None:
        test_trie = bartez_trie_import_from_file(get_test_dictionary_path(), "italian")
    return test_trie

def get_test_trie_small():
    global test_trie_small
    if test_trie_small is None:
        test_trie_small = bartez_trie_import_from_file(get_test_dictionary_path_1000(), "italian")
    return test_trie_small


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

    def test_bartez_trie_visitor_word_match(self):
        dictionary = get_test_trie()
        root = dictionary.get_root()
        match_visitor = BartezDictionaryTrieNodeVisitorWordMatch('zuzzurellone')
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

        print("Matching every word in dictionary")
        found = True
        for word in words:
            match_visitor = BartezDictionaryTrieNodeVisitorWordMatch(word)
            root.accept(match_visitor)
            found &= match_visitor.matches()

        print("Found every word in dictionary: " + str(found))

    def test_bartez_trie_visitor_word_not_match(self):
        dictionary = get_test_trie()
        root = dictionary.get_root()
        match_visitor = BartezDictionaryTrieNodeVisitorWordMatch('networkx')
        root.accept(match_visitor)
        found = match_visitor.matches()
        print("Word " + match_visitor.get_word() + " found: " + str(found))
        self.assertFalse(found)

    def test_bartez_trie_visitor_page_splitter(self):
        trie_loaded = bartez_trie_load_from_file("bartez_trie.btt")
        root = trie_loaded.get_root()
        page_splitter_visitor = BartezDictionaryTrieNodeVisitorPageSplitter()
        root.accept(page_splitter_visitor)
        pages = page_splitter_visitor.get_pages()
        print("Found " + str(len(pages)) + " pages")
        self.assertTrue(pages is not None)

    def test_bartez_trie_serialize(self):
        dictionary = get_test_trie()
        bartez_trie_save_to_file(dictionary, "bartez_trie.btt")
        trie_loaded = bartez_trie_load_from_file("bartez_trie.btt")
        self.assertTrue(trie_loaded is not None)


if __name__ == '__main__':
    unittest.main()
