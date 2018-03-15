from abc import ABCMeta, abstractmethod
from bartez.utils_solver import get_pattern
from bartez.solver.solver_observer import BartezObservable
from bartez.solver.solver_scenario import make_replica


class BartezNodeVisitor(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def visit_node(self, node, scenario):
        pass


class BartezClusterVisitorSolver(BartezNodeVisitor, BartezObservable):
    __metaclass__ = ABCMeta

    def __init__(self, matcher):
        BartezNodeVisitor.__init__(self)
        BartezObservable.__init__(self)
        self.__matcher = matcher

    def forward_check(self, node, scenario):
        graph = node.get_graph()

        replica = make_replica(scenario)

        for n in graph.neighbors(node.get_absolute_index()):
            neighbor_node = graph.nodes()[n]['bartez_node']
            neighbor_entry = neighbor_node.get_entry()
            pattern = get_pattern(neighbor_entry.absolute_index(), replica.entries)
            matches = self.__matcher.get_matches(pattern)
            if len(matches) == 0:
                return False

        return True


    def get_next_child(self, node, scenario):
        entry = node.get_entry()
        traverse_length = len(scenario.traverse_order)
        traverse_position = scenario.traverse_order.index(entry.absolute_index())
        if traverse_position + 1 >= traverse_length:
            return None

        next_position = traverse_position + 1
        next_to = scenario.traverse_order[next_position]
        next_node = node.get_graph().nodes[next_to]['bartez_node']
        return next_node


    def visit_node(self, node, scenario):
        entry = node.get_entry()

        if (entry.absolute_index() not in scenario.traverse_order):
            return True

        if entry.is_valid():
            return True

        replica = make_replica(scenario)
        self.notify_observers(replica.entries)

        next_node = self.get_next_child(node, replica)
        if next_node is None:
            return True

        entry_replica = replica.entries[entry.absolute_index()]

        pattern = get_pattern(entry.absolute_index(), replica.entries)
        matches = self.__matcher.get_matches(pattern)
        entry_replica.set_value(pattern)

#        if self.forward_check(node, replica) is False:
#            return False

#        if self.forward_check(next_node, replica) is False:
#            return False

        for match in matches:
            # trying a match

            if match in replica.used_words:
                continue

            entry_replica.set_value(match)
            entry_replica.set_is_valid(True)
            replica.used_words.append(match)

            if self.forward_check(node, replica) is False:
                continue

            if self.forward_check(next_node, replica) is False:
                continue

            if self.visit_node(next_node, replica):
                return True

            if match in replica.used_words:
                replica.used_words.remove(match)

            entry_replica.set_is_valid(False)
            entry_replica.set_value(entry.get_value())
            continue

        return False
