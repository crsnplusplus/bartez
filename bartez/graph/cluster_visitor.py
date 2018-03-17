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
            matches = self.__matcher.get_matches(pattern)
            if matches is None:
                return False

            if len(matches) < 2:
                return False

        return True


    def forward_check_neighbors(self, node, scenario):
        graph = node.get_graph()

        for n in graph.neighbors(node.get_absolute_index()):
            neighbor_node1 = graph.nodes()[n]['bartez_node']

            if neighbor_node1 is node:
                continue

            neighbor_entry1 = neighbor_node1.get_entry()
#            if neighbor_entry1.is_valid():
#                continue

            pattern1 = get_pattern(neighbor_entry1.absolute_index(), scenario.entries)

            if self.__matcher.is_bad_pattern(pattern1):
                return False

            for m in graph.neighbors(n):
                neighbor_node2 = graph.nodes()[m]['bartez_node']

                if neighbor_node2 is node:
                    continue

                if neighbor_node2 is neighbor_node1:
                    continue

                neighbor_entry2 = neighbor_node2.get_entry()
                if neighbor_entry2.is_valid():
                    continue

                pattern2 = get_pattern(neighbor_entry2.absolute_index(), scenario.entries)

                if self.__matcher.is_bad_pattern(pattern2):
                    return False

                matches = self.__matcher.get_matches(pattern2)
                if matches is None:
                    return False

                if len(matches) < 1:
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

    def visit_root(self, node, scenario):
        result_scenario, result = self.visit_node(node, scenario)
        return result_scenario, result

    def visit_node(self, node, scenario):
        entry = scenario.entries[node.get_absolute_index()]
        assert(entry.absolute_index() in scenario.traverse_order)

        next_node = self.get_next_child(node, scenario)
        if next_node is None:
            return scenario, True

        if entry.is_valid():
            return scenario, True

        pattern = get_pattern(entry.absolute_index(), scenario.entries)
        if self.__matcher.is_bad_pattern(pattern):
            return scenario, False

        if self.forward_check_neighbors(node, scenario) is False:
            return scenario, False

        if self.forward_check_neighbors(next_node, scenario) is False:
            return scenario, False

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

            result_scenario, result = self.visit_node(next_node, replica)
            if result is True:
                return result_scenario, True

            if match in replica.used_words:
                replica.used_words.remove(match)

            entry_replica.set_is_valid(False)
            old_value = entry.get_value()
            entry_replica.set_value(old_value)
            continue

        return replica, False
