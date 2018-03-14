from abc import ABCMeta, abstractmethod


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
