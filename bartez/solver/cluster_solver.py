import networkx as nx

from copy import copy

from bartez.solver.solver_observer import BartezObservable
from bartez.solver.solver_scenario import make_scenario, make_replica
from bartez.utils_solver import get_pattern
from bartez.graph.cluster_visitor import BartezClusterVisitorSolver


class BartezClusterSolver(BartezObservable):
    def __init__(self, container, container_entries, cluster_index, cluster, cluster_entries=None, matcher=None):
        BartezObservable.__init__(self)
        self.__container = container
        self.__container_entries = container_entries

        self.__cluster_index = cluster_index
        self.__cluster_graph = cluster

        self.__entries = cluster_entries
        self.__matcher = matcher

        self.__traverse_order = []
        self.__first_entry_index = 0

    def get_cluster_index(self):
        return self.__cluster_index

    def set_matcher(self, matcher):
        self.__matcher = matcher

    def set_entries(self, entries):
        self.__entries = entries

    def get_entries(self):
        return self.__entries

    def set_first_entry_index(self, first_entry_index):
        self.__first_entry_index = first_entry_index

    def get_num_of_vertex(self):
        return 0 if self.__cluster_graph is None else len(self.__cluster_graph.nodes())

    def run(self):
        self.__traverse_order = self.__get_traverse_order()
        self.__solve_backtracking(copy(self.__container_entries))

    def run_visitor(self, container_scenario):
        cluster_graph = self.__cluster_graph
        solver = BartezClusterVisitorSolver(self.__matcher)

        for o in self.get_observers():
            solver.register_observer(o)

        used_words = []
        traverse_order = self.__get_traverse_order()
        scenario = make_scenario(self.__container_entries,
                                 self.__cluster_graph,
                                 used_words,
                                 traverse_order,
                                 container_scenario.forbidden)

        first_node_index = traverse_order[0]
        first_traverse_node = cluster_graph.nodes[first_node_index]

        start_node = first_traverse_node['bartez_node']
        result = self.__back_track_visit(start_node, scenario, solver)

        for o in self.get_observers():
            solver.unregister_observer(o)

        return scenario, result


    def __back_track_visit(self, node, scenario, solver):
        #replica = make_replica(scenario)
        return node.accept(solver, scenario)

    def __get_first_entry(self):
        start = self.__first_entry_index
        #entry_index = self.__entries[start]
        return start

    def __get_traverse_order(self):
        #dfs = nx.dfs_tree(self.__graph, self.__get_first_entry())
        dfs = self.__cluster_graph
        dfs_to = list(nx.dfs_preorder_nodes(dfs))
        return dfs_to

    def run_scenario(self):
        used_words = []
        traverse_order = self.__get_traverse_order()
        scenario = make_scenario(self.__entries, self.__cluster_graph, used_words, traverse_order)
        self.__solve_backtracking_scenario(scenario)

    def __solve_backtracking_scenario(self, scenario):
        self.notify_observers(scenario.entries)

        for position in scenario.traverse_order:
            entry = scenario.entries[position]

            if entry.valid() is True:
                continue

            entry_absoulte_index = entry.absolute_index()
            pattern = get_pattern(entry_absoulte_index, scenario.entries)
            matches = copy(self.__matcher.get_matches(pattern))

            replica = copy(scenario)
            entry_replica = replica.entries[entry_absoulte_index]

            for match in matches:
                # trying a match
                entry_replica.set_value(match)
                entry_replica.set_is_valid(True)

                if self.__solve_backtracking_scenario(replica):
                    return True

                entry_replica.set_is_valid(False)
                continue

            return False  # backtracking

        return True

    def __solve_backtracking(self, entries):
        self.notify_observers(entries)

        traverse_order = self.__traverse_order

        for position in traverse_order:
            entry = entries[position]

            if entry.valid() is True:
                continue

            entry_absoulte_index = entry.absolute_index()
            pattern = get_pattern(entry_absoulte_index, entries)
            matches = copy(self.__matcher.get_matches(pattern))
            # matches = get_matches(self.__dictionary, pattern, used_words)

            entries_copy = copy(entries)
            entry_copy = entries_copy[entry_absoulte_index]

            for match in matches:
                # trying a match
                entry_copy.set_value(match)
                entry_copy.set_is_valid(True)

                if self.__solve_backtracking(entries_copy):
                    return True

                entry_copy.set_is_valid(False)
                continue

            return False  # backtracking

        return True
