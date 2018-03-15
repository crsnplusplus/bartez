from abc import ABCMeta, abstractmethod


class BartezGraphNodeVisitor(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def visit_entry(self, node):
        pass


class BartezGraphNodeVisitorSolver(BartezGraphNodeVisitor):
    __metaclass__ = ABCMeta
    def __init__(self):
        BartezGraphNodeVisitor.__init__(self)

    def visit_entry(self, node):
        entry = node.get_entry()
        graph = node.get_graph()
        entries = graph.get_local_entries()
        container_entries = graph.get_container_entries()

        neighbors = graph.neighbors(node.get_absolute_index())
        for neigh in neighbors:
            print(neigh)
        return entry
