from abc import ABCMeta, abstractmethod

from bartez.dictionary.trie_node import BartezDictionaryTrieNodeTerminal, BartezDictionaryTrieNodeNonTerminal


class BartezDictionaryTrie(object):
    __metaclass__ = ABCMeta

    def __init__(self, language):
        self.__language = language
        self.__root = BartezDictionaryTrieNodeNonTerminal(None, '')
        self.__count = 0

    def get_language(self):
        return self.__language

    def get_root(self):
        return self.__root

    def is_loaded(self):
        return self.__root is not None

    def word_count(self):
        return self.__count

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
            self.__count += 1


    @abstractmethod
    def remove_word(self, word):
        last_node = self.__root

        for pos in range(len(word)):
            current_char = word[pos]
            child = last_node.get_child(current_char)
            assert(child is not None)
            last_node = child

        assert(last_node.has_terminal())
        last_node.remove_child(last_node.get_child('#'))
        self.__count -= 1

        while last_node is not self.__root:
            if last_node.has_children():
                break

            node_to_remove = last_node
            last_node = last_node.get_parent()
            last_node.remove_child(node_to_remove)
