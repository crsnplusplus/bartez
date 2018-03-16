import unittest

from bartez.dictionary.trie_node_visitor import BartezDictionaryTrieNodeVisitorPageSplitter
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
        matches = matcher.get_matches(pattern_searched)

        print("Found " + str(len(matches)) + " for pattern: " + pattern_searched )
        for match in matches:
            print("  " + match)
        return

if __name__ == '__main__':
    unittest.main()
