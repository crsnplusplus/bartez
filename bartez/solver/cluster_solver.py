import networkx as nx

from copy import copy

from bartez.solver.solver_observer import BartezObservable
from bartez.utils_solver import get_pattern, are_there_enough_matches, get_entries_intersection


class BartezClusterSolver(BartezObservable):
    def __init__(self, index, matcher=None, entries=None, container_entries=None ,graph=None):
        BartezObservable.__init__(self)
        self.__index = index,
        self.__matcher = matcher
        self.__entries = entries
        self.__container_entries = container_entries
        self.__graph = graph
        self.__traverse_order = []
        self.__first_entry_index = 0
        return

    def get_index(self):
        return self.__index

    def set_matcher(self, matcher):
        self.__matcher = matcher

    def set_entries(self, entries):
        self.__entries = entries

    def set_container_entries(self, container_entries):
        self.__container_entries = container_entries

    def set_graph(self, graph):
        self.__graph = graph

    def set_first_entry_index(self, first_entry_index):
        self.__first_entry_index = first_entry_index

    def get_num_of_vertex(self):
        return 0 if self.__graph is None else len(self.__graph.nodes())

    def run(self):
        self.__traverse_order = self.__get_traverse_order()
        self.__solve_backtracking(self.__container_entries)

    def __get_first_entry(self):
        start = self.__first_entry_index
        #entry_index = self.__entries[start]
        return start

    def __get_traverse_order(self):
        #dfs = nx.dfs_tree(self.__graph, self.__get_first_entry())
        dfs = nx.dfs_tree(self.__graph)
        dfs_to = list(nx.dfs_preorder_nodes(dfs))
        return dfs_to

    def __solve_backtracking(self, entries):
        self.notify_observers(entries)

        traverse_order = self.__traverse_order

        for position in traverse_order:
            entry = entries[position]

            if entry.valid() is True:
                continue

            entry_absoulte_index = entry.absolute_index()
            pattern = get_pattern(entry_absoulte_index, entries)
            matches = self.__matcher.get_matches(pattern)
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

    def __solve_backtracking_old(self, entries):
        traverse_order = self.__traverse_order
        used_words = []
        for position, entry_index in enumerate(traverse_order):
            assert (traverse_order[position] == entry_index)
            entry = entries[entry_index]

            if entry.valid() is True:
                used_words.append(entry.value())
                continue

            pattern = get_pattern(entry_index, entries)
            matches = self.__matcher.get_matches(pattern)
            # matches = get_matches(self.__dictionary, pattern, used_words)

            entries_copy = copy(entries)
            entry_copy = entries_copy[entry_index]

            for match in matches:
                # trying a match
                entry_copy.set_value(match)
                entry_copy.set_is_valid(True)
                used_words_copy = copy(used_words)
                used_words_copy.append(match)

                #                if self.__forward_check(self.__dictionary,
                #                                        used_words_copy,
                #                                        entry_index,
                #                                        entries_copy) == False:
                #                    continue

                used_words.append(match)

                if self.__solve_backtracking(entries_copy):
                    return True
                # that branch didn't go well, trying next
                entries_copy[entry_index] = entries[entry_index]
                entry_copy.set_is_valid(False)
                used_words.pop()

            return False  # backtracking
        return True

    def __forward_check(self, dictionary, used_words, entry_index, entries, descend=True):
        entry = entries[entry_index]
        pattern = entry.value()

        for relation_index, relation in enumerate(entry.relations()):
            pattern_as_list = list(pattern)
            other = entries[relation.index()]
            if other.is_valid() == True:
                continue

            other_pattern_as_list = list(other.value())

            pos_in_entry, pos_in_other = get_entries_intersection(relation.coordinate(), entry, other)
            other_pattern_as_list[pos_in_other] = pattern_as_list[pos_in_entry]

            other_pattern = "".join(other_pattern_as_list)

            if are_there_enough_matches(dictionary, other_pattern, used_words, 1) == False:
                return False

        return True

    def __build_pattern(self, dictionary, used_words, entry_index, entries):
        entry = entries[entry_index]
        pattern = entry.value()

        for relation_index, relation in enumerate(entry.relations()):
            pattern_as_list = list(pattern)
            other_index = relation.index()
            other = entries[other_index]
            other_pattern_as_list = list(other.value())

            pos_in_entry, pos_in_other = get_entries_intersection(relation.coordinate(), entry, other)
            other_pattern_as_list[pos_in_other] = pattern_as_list[pos_in_entry]

            other_pattern = "".join(other_pattern_as_list)

            if are_there_enough_matches(dictionary, other_pattern, used_words, 2) == False:
                return False

        return True
