import unittest

from bartez.dictionary.trie_node_visitor import *
from bartez.tests.test_utils import *

class TestBartezTrie(unittest.TestCase):

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