from abc import ABCMeta, abstractmethod


class BartezTrieNode(object):
    __metaclass__ = ABCMeta

    """Trie Node used by BartezTrie class"""
    def __init__(self, parent, char):
        self.__char = char
        self.__parent = parent


    def get_char(self):
        return self.__char


    def get_parent(self):
        return self.__parent


    @abstractmethod
    def accept(self, visitor):
        pass


class BartezNodeNonTerminal(BartezTrieNode):
    """Trie Node Non Terminal used by BartezTrie class"""
    def __init__(self, parent, char):
        BartezTrieNode.__init__(self, parent, char)
        self.__children = { }


    def get_children(self):
        return self.__children


    def accept(self, visitor):
        visitor.visit_non_terminal(self)


    def get_child(self, char):
        return self.__children[char] if char in self.__children else None

    def has_terminal(self):
        return True if self.get_child('#') is not None else False


    def has_children(self):
        return len(self.__children) > 0


    def add_child(self, child):
        assert(self.get_child(child.get_char()) is None)
        self.__children[child.get_char()] = child


class BartezNodeTerminal(BartezTrieNode):
    """Trie Node Terminal used by BartezTrie class"""
    def __init__(self, parent):
        BartezTrieNode.__init__(self, parent, '#')

    def accept(self, visitor):
        visitor.visit_terminal(self)

