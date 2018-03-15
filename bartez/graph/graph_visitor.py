from abc import ABCMeta, abstractmethod


class BartezGraphNodeVisitor(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def visit_entry(self, node):
        pass


class BartezGraphNodeVisitorSolver(BartezGraphNodeVisitor):
    __metaclass__ = ABCMeta

    def __init__(self, matcher):
        BartezGraphNodeVisitor.__init__(self)
        self.__matcher = matcher

    def visit_entry(self, node):
        entry = node.get_entry()
        graph = node.get_graph()
        neighbors = list(graph.neighbors(node.get_absolute_index()))

        entries = graph.get_local_entries()
        container_entries = graph.get_container_entries()

        print("+ " + str(entry.get_description()))
        for n in neighbors:
            neighbor = graph.get_container_entries()[n]
            print("  - " + str(neighbor.get_description()))

        for n in neighbors:
            neighbor = graph.get_container_entries()[n]
            if neighbor is entry:
                continue

            neighbor_node = graph.nodes()[n]['bartez_node']
            neighbor_node.accept(self)

        return entry
