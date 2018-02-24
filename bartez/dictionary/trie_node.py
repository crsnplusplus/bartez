from abc import ABCMeta, abstractmethod


class BartezNode(object):
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


class BartezNodeNonTerminal(BartezNode):
    """Trie Node Non Terminal used by BartezTrie class"""
    def __init__(self, parent, char):
        BartezNode.__init__(self, parent, char)
        self.__children = []

    def get_children(self):
        return self.__children

    def accept(self, visitor):
        visitor.visit_non_terminal(self)

    def get_child(self, char):
        for child in self.__children:
            if child.get_char() == char:
                return child

        return None

    def has_terminal(self):
        for child in self.__children:
            if child.get_char() == '#':
                return True

        return False

    def has_children(self):
        return len(self.__children) > 0

    def add_child(self, child):
        assert(self.get_child(child.get_char()) == None)
        self.__children.append(child)

class BartezNodeTerminal(BartezNode):
    """Trie Node Terminal used by BartezTrie class"""
    def __init__(self, parent):
        BartezNode.__init__(self, parent, '#')

    def accept(self, visitor):
        visitor.visit_terminal(self)

