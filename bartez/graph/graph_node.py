from abc import ABCMeta, abstractmethod


class BartezGraphNodeVisitable(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def accept(self, visitor, scenario):
        pass


class BartezGraphNodeVisitableEntry(BartezGraphNodeVisitable):
    __metaclass__ = ABCMeta

    def __init__(self, absolute_index, entry, description, graph):
        BartezGraphNodeVisitable.__init__(self)
        self.__absolute_index = absolute_index
        self.__entry = entry
        self.__description = description
        self.__graph = graph

    def get_absolute_index(self):
        return self.__absolute_index

    def get_entry(self):
        return self.__entry

    def get_description(self):
        return self.__description

    def get_graph(self):
        return self.__graph

    def accept(self, visitor, scenario):
        return visitor.visit_node(self, scenario)
