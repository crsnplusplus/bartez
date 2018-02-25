from abc import ABCMeta, abstractmethod


class BartezNodeVisitor(object):
    __metaclass__ = ABCMeta

    def __get_distance_with_parent(self, node, parent_searched):
        parent = node.get_parent()

        distance = 0

        while parent is not None:
            distance += 1

            if parent == parent_searched:
                return distance

            parent = parent.get_parent()

        return -1

    @abstractmethod
    def visit_non_terminal(self, node):
        pass

    @abstractmethod
    def visit_terminal(self, node):
        pass


class BartezNodeVisitorPrint(BartezNodeVisitor):
    def visit(self, node):
        node.accept(self)


    def visit_non_terminal(self, node):
        children = node.get_children()

        for child in node.get_children():
            child.accept(self)


    def visit_terminal(self, node):
        parent = node.get_parent()

        word = ""

        while parent is not None:
            word = parent.get_char() + word
            parent = parent.get_parent()

        print("found word: " + word)


class BartezNodeVisitorList(BartezNodeVisitor):
    def __init__(self):
        self.__list = []

    def visit(self, node):
        node.accept(self)


    def visit_non_terminal(self, node):
        children = node.get_children()

        for child in node.get_children():
            child.accept(self)


    def visit_terminal(self, node):
        parent = node.get_parent()

        word = ""

        while parent is not None:
            word = parent.get_char() + word
            parent = parent.get_parent()

        self.__list.append(word)


    def get_words(self):
        return self.__list