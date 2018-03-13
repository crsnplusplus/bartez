import networkx as nx

from copy import copy

from bartez.utils_solver import get_pattern, get_matches, are_there_enough_matches, get_entries_intersection


class BartezClusterSolver:
    def __init__(self, dictionary=None, entries=None, graph=None):
        self.__dictionary = dictionary
        self.__entries = entries
        self.__graph = graph
        self.__traverse_order = []

    def set_dictionary(self, dictionary):
        self.__dictionary = dictionary

    def set_entries(self, entries):
        self.__entries = entries

    def set_graph(self, graph):
        self.__graph = graph

    def get_num_of_vertex(self):
        return 0 if self.__graph is None else len(self.__graph.nodes())

    def run(self):
        self.__traverse_order = self.__get_traverse_order()
        self.__solve_backtracking(self.__entries)

    def __get_traverse_order(self):
        bfs = nx.dfs_tree(self.__graph, 0)
        bfs_to = list(nx.dfs_preorder_nodes(bfs))
        return bfs_to

    def __solve_backtracking(self, entries):
        traverse_order = self.__traverse_order
        used_words = []
        for position, entry_index in enumerate(traverse_order):
            assert (traverse_order[position] == entry_index)
            entry = entries[entry_index]

            if entry.valid() is True:
                used_words.append(entry.value())
                continue

            pattern = get_pattern(entry_index, entries)
            matches = get_matches(self.__dictionary, pattern, used_words)

            entries_copy = copy(entries)
            entry_copy = entries_copy[entry_index]

            for match in matches:
                # trying a match
                entry_copy.set_value(match)
                entry_copy.set_is_valid(True)
                used_words_copy = copy(used_words)
                used_words_copy.append(match)

                if self.__forward_check(self.__dictionary,
                                        used_words_copy,
                                        entry_index,
                                        entries_copy) == False:
                    continue

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
