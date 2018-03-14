from abc import ABCMeta, abstractmethod

from bartez.dictionary.trie_node import BartezDictionaryTrieNodeTerminal, BartezDictionaryTrieNodeNonTerminal


class BartezDictionaryTrie(object):
    __metaclass__ = ABCMeta

    def __init__(self, language):
        self.__language = language
        self.__root = BartezDictionaryTrieNodeNonTerminal(None, '')

    def get_language(self):
        return self.__language

    def get_root(self):
        return self.__root

    def is_loaded(self):
        return self.__root is not None

    @abstractmethod
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
