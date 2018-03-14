from bartez.dictionary.trie import BartezDictionaryTrie


class BartezDictionaryTriePatternMatcher(object):
    def __init__(self):
        self.__dictionaries_by_word_length = { }
        self.__dictionaries = self.__dictionaries_by_word_length




'''
    def add_word(self, word):
        parent = self.__root

        for pos in range(len(word)):
            current_char = word[pos]
            child = parent.get_child(current_char)
            if child is None:
                child = BartezDictionaryTrieNodeNonTerminal(parent, current_char)
                parent.add_child(child)

            parent = child

        if parent.has_terminal() is False:
            child = BartezDictionaryTrieNodeTerminal(parent)
            parent.add_child(child)
'''