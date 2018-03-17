from bartez.dictionary.trie import BartezDictionaryTrie
from bartez.dictionary.trie_node_visitor import BartezDictionaryTrieNodeVisitorMatchPattern
from bartez.dictionary.trie_node_visitor import BartezDictionaryTrieNodeVisitorPageSplitter


class BartezDictionaryTriePage(BartezDictionaryTrie):

    def __init__(self, language, page_number):
        BartezDictionaryTrie.__init__(self, language)
        self.__page_number = page_number

    def add_word(self, word):
        BartezDictionaryTrie.add_word(self, word)

    def get_page_number(self):
        return self.__page_number


class BartezDictionaryTriePatternMatcher(object):

    def __init__(self, collect=True):
        self.__language = ''
        # this is  a reminder: self.__pages *are* dictionaries_by_word_length
        dictionaries_by_word_length = { }
        self.__pages = dictionaries_by_word_length
        self.__match_visitor = BartezDictionaryTrieNodeVisitorMatchPattern()
        self.__bad_patterns = []
        self.__collect = collect

    def set_language(self, language):
        self.__language = language

    def get_language(self):
        return self.__language

    def load_from_dictionary_trie(self, dictionary_trie):
        page_splitter_visitor = BartezDictionaryTrieNodeVisitorPageSplitter()
        page_splitter_visitor.visit(dictionary_trie.get_root())
        pages = page_splitter_visitor.get_pages()
        for page_key, page_value in pages.items():
            self.add_page(page_value, page_key)
        return

    def add_page(self, page, page_index):
        if page_index not in self.__pages:
            self.__pages[page_index] = BartezDictionaryTriePage(self.__language, page_index)

        dictionary_page = self.__pages[page_index]
        for word in page:
            assert(len(word) == page_index)
            dictionary_page.add_word(word)

    def get_matches(self, pattern):
        if pattern in self.__bad_patterns:
            return None

        pattern_length = len(pattern)
        dictionary_page = self.__pages[pattern_length]
        assert(pattern_length == dictionary_page.get_page_number())
        self.__match_visitor.set_pattern(pattern)
        self.__match_visitor.visit(dictionary_page.get_root())

        matches = self.__match_visitor.detach_matches()
        if matches is None or len(matches) == 0:
            self.mark_pattern_as_bad(pattern)

        return matches

    def mark_pattern_as_bad(self, pattern):
        if pattern.count('.') == 0:
            return

        if pattern in self.__bad_patterns:
            return

        self.__bad_patterns.append(pattern)


    def is_bad_pattern(self, pattern):
        return pattern in self.__bad_patterns