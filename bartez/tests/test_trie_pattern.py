import unittest

from bartez.dictionary.trie_node_visitor import BartezDictionaryTrieNodeVisitorPageSplitter
from bartez.dictionary.trie_node_visitor import BartezDictionaryTrieNodeVisitorList
from bartez.tests.test_utils import *


class TestBartezTriePattern(unittest.TestCase):

    def test_bartez_trie_visitor_match_pattern(self):
        trie_loaded = bartez_trie_load_from_file("bartez_trie.btt")
        root = trie_loaded.get_root()
        page_splitter_visitor = BartezDictionaryTrieNodeVisitorPageSplitter()
        root.accept(page_splitter_visitor)
        pages = page_splitter_visitor.get_pages()
        print("Found " + str(len(pages)) + " pages")
        self.assertTrue(pages is not None)

        matcher = BartezDictionaryTriePatternMatcher()
        matcher.set_language(trie_loaded.get_language())

        for page_key, page_value in pages.items():
            matcher.add_page(page_value, page_key)

        pattern_searched = 'savonarol.'
        used_words = []
        matches = matcher.get_matches(pattern_searched, used_words)

        print("Found " + str(len(matches)) + " for pattern: " + pattern_searched )
        for match in matches:
            print("  " + match)
        return


    def test_bartez_trie_add_remove(self):
        trie_loaded = bartez_trie_load_from_file("bartez_trie.btt")
        self.assertTrue(trie_loaded.is_loaded() is True)
        word = "ABCDE"
        trie_loaded.add_word(word)
        trie_loaded.remove_word(word)
        list_visitor = BartezDictionaryTrieNodeVisitorList()
        root = trie_loaded.get_root()
        root.accept(list_visitor)
        words = list_visitor.get_words()
        self.assertTrue(len(words) == 281614)

if __name__ == '__main__':
    unittest.main()
