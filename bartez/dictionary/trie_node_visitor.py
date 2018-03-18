from abc import ABCMeta, abstractmethod
from copy import copy


class BartezDictionaryTrieNodeVisitor(object):
    __metaclass__ = ABCMeta

    def get_distance_with_root(self, node):
        parent = node.get_parent()

        distance = 0

        while parent is not None:
            distance += 1
            parent = parent.get_parent()

        return distance

    @abstractmethod
    def visit_non_terminal(self, node):
        pass

    @abstractmethod
    def visit_terminal(self, node):
        pass


class BartezDictionaryTrieNodeVisitorPrint(BartezDictionaryTrieNodeVisitor):
    def visit(self, node):
        node.accept(self)


    def visit_non_terminal(self, node):
        for child in node.get_children().items():
            child[1].accept(self)


    def visit_terminal(self, node):
        parent = node.get_parent()

        word = ""

        while parent is not None:
            word = parent.get_char() + word
            parent = parent.get_parent()

        print("found word: " + word)


class BartezDictionaryTrieNodeVisitorList(BartezDictionaryTrieNodeVisitor):
    def __init__(self):
        self.__list = []

    def visit(self, node):
        node.accept(self)

    def visit_non_terminal(self, node):
        for child in node.get_children().items():
            child[1].accept(self)

    def visit_terminal(self, node):
        parent = node.get_parent()

        word = ""

        while parent is not None:
            word = parent.get_char() + word
            parent = parent.get_parent()

        self.__list.append(word)

    def get_words(self):
        return self.__list


class BartezDictionaryTrieNodeVisitorNodeCounter(BartezDictionaryTrieNodeVisitor):
    def __init__(self):
        self.__non_terminal_count = 0
        self.__terminal_count = 0

    def visit(self, node):
        node.accept(self)


    def visit_non_terminal(self, node):
        self.__non_terminal_count += 1

        for child in node.get_children().items():
            child[1].accept(self)


    def visit_terminal(self, node):
        self.__terminal_count += 1


    def get_terminal_count(self):
        return self.__terminal_count


    def get_non_terminal_count(self):
        return self.__non_terminal_count

    def get_nodes_count(self):
        return self.__terminal_count + self.__non_terminal_count


class BartezDictionaryTrieNodeVisitorMatchWord(BartezDictionaryTrieNodeVisitor):
    def __init__(self, word):
        self.__word = word.upper()
        self.__matches = False

    def get_word(self):
        return self.__word

    def matches(self):
        return self.__matches


    def visit(self, node):
        node.accept(self)


    def visit_non_terminal(self, node):
        pos = self.get_distance_with_root(node)
        children = node.get_children()

        letter = '#' if pos == len(self.__word) else self.__word[pos]
        assert(pos <= len(self.__word))

        if letter not in children:
            self.__matches = False
            return

        children[letter].accept(self)
        return


    def visit_terminal(self, node):
        self.__matches = True


class BartezDictionaryTrieNodeVisitorMatchPattern(BartezDictionaryTrieNodeVisitor):
    def __init__(self, pattern=''):
        self.__pattern = pattern
        self.__matches = []
        self.__min_matches_count = 0

    def set_pattern(self, pattern):
        self.__matches.clear()
        self.__pattern = pattern.upper()

    def get_pattern(self):
        return self.__pattern

    def get_matches(self):
        if self.__matches is None:
            return []

        return self.__matches

    def detach_matches(self):
        matches = copy(self.__matches)
        return matches

    def visit(self, node):
        node.accept(self)

    def visit_non_terminal(self, node):
        pos = self.get_distance_with_root(node)
        children = node.get_children()

        letter = '#' if pos == len(self.__pattern) else self.__pattern[pos]
        assert(pos <= len(self.__pattern))

        if letter in children:
            # so far, so good. continue ...
            child = children[letter]
            child.accept(self)
            return

        if letter is '.':
            # continue for every child
            for child in children:
                children[child].accept(self)

        # not found!
        return

    def visit_terminal(self, node):
        self.__add_word_to_matches(node)

    def __add_word_to_matches(self, terminal_node):
        current_node = terminal_node.get_parent()
        word = ""

        while current_node is not None:
            word = current_node.get_char() + word
            current_node = current_node.get_parent()

        self.__matches.append(word)

class BartezDictionaryTrieNodeVisitorSingleMatchPattern(BartezDictionaryTrieNodeVisitor):
    def __init__(self, pattern=''):
        self.__pattern = pattern
        self.__matches = False

    def set_pattern(self, pattern):
        self.__pattern = pattern.upper()

    def get_pattern(self):
        return self.__pattern

    def has_match(self):
        return self.__matches

    def reset(self):
        self.__matches = False

    def visit(self, node):
        node.accept(self)

    def visit_non_terminal(self, node):
        if self.__matches is True:
            return

        pos = self.get_distance_with_root(node)
        children = node.get_children()

        letter = '#' if pos == len(self.__pattern) else self.__pattern[pos]
        assert(pos <= len(self.__pattern))

        if letter in children:
            # so far, so good. continue ...
            child = children[letter]
            child.accept(self)
            return

        if letter is '.':
            # continue for every child
            for child in children:
                children[child].accept(self)
                if self.__matches is True:
                    return

        # not found!
        return

    def visit_terminal(self, node):
        self.__matches = True


class BartezDictionaryTrieNodeVisitorPageSplitter(BartezDictionaryTrieNodeVisitor):
    def __init__(self):
        self.__pages = {}

    def get_page_number(self, number):
        return self.__pages[number]

    def visit(self, node):
        node.accept(self)

    def visit_non_terminal(self, node):
        for child in node.get_children().items():
            child[1].accept(self)

    def visit_terminal(self, node):
        parent = node.get_parent()

        word = ""

        while parent is not None:
            word = parent.get_char() + word
            parent = parent.get_parent()

        page_number = len(word)
        pos = self.get_distance_with_root(node)
        assert(page_number == pos - 1) # without the terminator!

        if page_number not in self.__pages:
            self.__pages[page_number] = []

        page = self.__pages[page_number]
        page.append(word)
        self.__pages[page_number] = page

    def get_pages(self):
        return self.__pages
