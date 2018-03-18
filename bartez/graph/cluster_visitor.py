from abc import ABCMeta, abstractmethod

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

    def _get_children_by_length(self, node, scenario):
        graph = node.get_graph()

        entries = []
        for n in graph.neighbors(node.get_absolute_index()):
            neighbor_entry = scenario.entries[n]
            entries.append((neighbor_entry.get_length(), n, neighbor_entry))

        entries_s = sorted(entries, key=lambda entry : entry[0])
        return [ (x[1], x[2]) for x in entries_s ]

    def get_next_child(self, node, scenario):
        graph = node.get_graph()

        if not scenario.path:
            return node

        for path_node_index in scenario.path:
            path_node = graph.nodes()[path_node_index]['bartez_node']

            children = self._get_children_by_length(path_node, scenario)
            for n, child_entry in children:
                if child_entry.is_valid() is True:
                    continue

                return graph.nodes()[n]['bartez_node']

        return None

    def _get_next_child(self, node, scenario):
        entry = node.get_entry()
        traverse_length = len(scenario.node_list)
        traverse_position = scenario.node_list.index(entry.absolute_index())
        if traverse_position + 1 >= traverse_length:
            return None

        next_position = traverse_position + 1
        next_to = scenario.node_list[next_position]
        next_node = node.get_graph().nodes[next_to]['bartez_node']
        return next_node

    def visit_root(self, node, scenario):
        result_scenario, result = self.visit_node(node, scenario)
        return result_scenario, result

    def visit_node(self, node, scenario):
        node_index = node.get_absolute_index()

        entry = scenario.entries[node_index]
        assert(entry.absolute_index() in scenario.node_list)

        pattern = entry.get_pattern(scenario.entries)

        replica = make_replica(scenario)
        entry_replica = replica.entries[entry.absolute_index()]
        entry_replica.set_value(pattern)

        replica.path.append(entry_replica.absolute_index())

        matches = self.__matcher.get_matches(pattern)
        old_value = entry.get_value()

        for match in matches:
            # trying a match

            if match in replica.used_words:
                continue

            entry_replica.set_value(match)
            entry_replica.set_is_valid(True)
            replica.used_words.append(match)
            self.notify_observers(replica.entries)

            next_node = self.get_next_child(node, replica)
            if next_node is None:
                return replica, True

            result_scenario, result = self.visit_node(next_node, replica)

            if result is True:
                return result_scenario, True

            if match in replica.used_words:
                replica.used_words.remove(match)

            entry_replica.set_is_valid(False)
            entry_replica.set_value(old_value)

        bjinfo = self.get_backjump_info(entry, entry_replica, pattern, scenario)

        entry_replica.set_is_valid(False)
        entry_replica.set_value(old_value)
        return scenario, False

    def get_backjump_info(self, entry, replica, pattern, scenario):
        analysys = []

        return analysys
