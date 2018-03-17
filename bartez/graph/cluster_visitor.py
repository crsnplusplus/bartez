from abc import ABCMeta, abstractmethod

from bartez.utils_solver import get_pattern
from bartez.solver.solver_observer import BartezObservable
from bartez.solver.solver_scenario import make_replica


class BartezNodeVisitor(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def visit_root(self, node, scenario):
        pass

    @abstractmethod
    def visit_node(self, node, scenario):
        pass


class BartezClusterVisitorSolver(BartezNodeVisitor, BartezObservable):
    __metaclass__ = ABCMeta

    def __init__(self, matcher):
        BartezNodeVisitor.__init__(self)
        BartezObservable.__init__(self)
        self.__matcher = matcher
        self.__backjump_index = None

    def forward_check(self, node, scenario):
        graph = node.get_graph()

        for n in graph.neighbors(node.get_absolute_index()):
            neighbor_node = graph.nodes()[n]['bartez_node']

            if node is neighbor_node:
                continue

            neighbor_entry = neighbor_node.get_entry()
            if neighbor_entry.is_valid():
                continue

            pattern = get_pattern(neighbor_entry.absolute_index(), scenario.entries)
            if self.__matcher.has_match(pattern) is False:
                return False

        return True

    def __should_backjump(self, node, scenario):
        #graph = node.get_graph()
        node_index = node.get_absolute_index()
        current_node_pos = scenario.traverse_order.index(node_index)
        #path = scenario.traverse_order[:current_node_pos]
        for to_node in scenario.traverse_order:
            to_entry = scenario.entries[to_node]
            if to_entry.is_valid():
                continue

            pattern = get_pattern(to_entry.absolute_index(), scenario.entries)
            matches = self.__matcher.has_match(pattern)
            if matches is False:
                return True

        return False

    def __prepare_backjump(self, current_node_index, backjump_node_index, traverse_order):
        assert(current_node_index in traverse_order)
        current_node_pos = traverse_order.index(current_node_index)
        path = traverse_order[:current_node_pos]
        if backjump_node_index not in path:
            return

        self.__backjump_index = backjump_node_index

    def __reset_backjump(self):
        self.__backjump_index = None

    def __will_backjump(self, current_node_index):
        if self.__backjump_index is None:
            return False

        return self.__backjump_index != current_node_index

    def forward_check_neighbors(self, node, scenario):
        graph = node.get_graph()
        node_index = node.get_absolute_index()

        for n in graph.neighbors(node_index):
            neighbor_node1 = graph.nodes()[n]['bartez_node']

            if neighbor_node1 is node:
                continue

            for m in graph.neighbors(n):
                neighbor_node2 = graph.nodes()[m]['bartez_node']

                if neighbor_node2 is node:
                    continue

                if neighbor_node2 is neighbor_node1:
                    continue

                neighbor_entry2 = neighbor_node2.get_entry()
                pattern2 = get_pattern(neighbor_entry2.absolute_index(), scenario.entries)

#                if self.__matcher.is_bad_pattern(pattern2):
#                    return False

                if self.__matcher.has_match(pattern2) is False:
                    return False

        return True


    def _get_next_child(self, node, scenario):
        node.get_graph()
        graph = node.get_graph()
        neighbor = None
        length_min = None

        for n in graph.neighbors(node.get_absolute_index()):
            neighbor_node = graph.nodes()[n]['bartez_node']
            neighbor_entry = neighbor_node.get_entry()
            neighbor_absolute_index = neighbor_node.get_absolute_index()
            if neighbor_absolute_index not in scenario.traverse_order:
                continue

            if neighbor_entry.is_valid() is True:
                continue

            entry_length = neighbor_entry.get_length()
            if length_min is None:
                length_min = entry_length

            if length_min > entry_length:
                neighbor = n
                length_min = entry_length

        if neighbor is None:
            return None

        return graph.nodes()[neighbor]['bartez_node']

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

    def visit_root(self, node, scenario):
        result_scenario, result = self.visit_node(node, scenario)
        return result_scenario, result

    def visit_node(self, node, scenario):
        node_index = node.get_absolute_index()

        entry = scenario.entries[node_index]
        assert(entry.absolute_index() in scenario.traverse_order)

        next_node = self.get_next_child(node, scenario)
        if next_node is None:
            return scenario, True

        if entry.is_valid():
            return scenario, True

        pattern = get_pattern(entry.absolute_index(), scenario.entries)
        if self.__matcher.is_bad_pattern(pattern):
            return scenario, False

#        if self.forward_check_neighbors(node, scenario) is False:
#            return scenario, False

#        if self.forward_check_neighbors(next_node, scenario) is False:
#            return scenario, False

#        if self.__should_backjump(node, scenario):
#            return scenario, False

        replica = make_replica(scenario)
        entry_replica = replica.entries[entry.absolute_index()]
        matches = self.__matcher.get_matches(pattern)

        if len(matches) == 0:
            self.__matcher.mark_pattern_as_bad(pattern)

        for match in matches:
            # trying a match

            if match in replica.used_words:
                continue

            entry_replica.set_value(match)
            entry_replica.set_is_valid(True)
            replica.used_words.append(match)
            self.notify_observers(replica.entries)

            if self.forward_check_neighbors(node, replica) is False:
                return scenario, False

#            if self.forward_check_neighbors(next_node, replica) is False:
#                return scenario, False

            result_scenario, result = self.visit_node(next_node, replica)

            if result is True:
                if self.__should_backjump(node, replica):
                    return scenario, False

                if self.__should_backjump(next_node, replica):
                    return replica, False

                return result_scenario, True

            if match in replica.used_words:
                replica.used_words.remove(match)

            entry_replica.set_is_valid(False)
            old_value = entry.get_value()
            entry_replica.set_value(old_value)

        return scenario, False
