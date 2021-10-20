import networkx as nx

from bartez.crossword import Square
"""from networkx.algorithms.community import *"""
from copy import copy
from bartez.utils_plot import save_graph_to_image
from bartez.utils_debug import print_crossword
from bartez.utils_solver import get_pattern, get_entries_intersection
from bartez.symbols import SquareValues, Symbols

from bartez.dictionary.trie_dust import DustDictionaryTriePatternMatcher, dust_trie_import_from_file
import bartez.tests.test_utils as test_utils
from dustpy import Trie, TrieWithPagesByLength, TrieWithPagesByLengthRobinMap, TrieWithPagesByLengthHopscotchMap


class CrosswordSolverDust(object):
    def __init__(self, dictionary=None, crossword=None):
        self.__dictionary = dictionary
        self.__crossword = crossword
        self.__graph = None
        self.__traverse_order = []
        dictionary_path = test_utils.get_test_dictionary_path()
        self.__matcher = dust_trie_import_from_file(dictionary_path, SquareValues.char, SquareValues.block)
        self.__used_words = DustDictionaryTriePatternMatcher(TrieWithPagesByLengthHopscotchMap(ord(SquareValues.char), ord(SquareValues.block)))
        self.__iterations = 0
        self.__update_frequency = 1


    def set_dictionary(self, dictionary):
        self.__dictionary = dictionary


    def set_crossword(self, crossword):
        self.__crossword = crossword


    def get_num_of_vertex(self):
        return 0 if self.__graph is None else len(self.__graph.nodes())


    def __create_graph_x(self):
        graph = nx.Graph()
        entries = self.__crossword.entries()
        self.__num_of_vertex = len(entries)

        for index_entry, entry in enumerate(entries):
            graph.add_node(index_entry, desc=str(entry.description()))
            relations = entry.relations()
            for index_relation, relation in enumerate(relations):
                graph.add_edge(index_entry, relation.index())

        self.__graph = graph
        self.__traverse_order = self.__get_traverse_order()


    def __get_traverse_order(self):
        nodes = self.__graph.nodes()
        node_zero = self.__graph.nodes()[0]
        bfs = nx.dfs_tree(self.__graph, 0)
        bfs_to = list(nx.dfs_preorder_nodes(bfs))
        traverse_order = nx.dfs_preorder_nodes(self.__graph)
        #return list(traverse_order)
        return list(bfs_to)


    def __solve_backtracking(self, entries):
        traverse_order = self.__traverse_order
        used_words = []
        self.__iterations += 1
        for position, entry_index in enumerate(traverse_order):
            assert (traverse_order[position] == entry_index)
            entry = entries[entry_index]

            if entry.valid() is True:
                continue

            pattern = get_pattern(entry_index, entries)
            matches = self.__matcher.get_matches(pattern)

            entries_copy = copy(entries)
            entry_copy = entries_copy[entry_index]

            for match in matches:
                # trying a match
                entry_copy.set_value(match)
                entry_copy.set_is_valid(True)

                if self.__forward_check(entry_index, entries_copy) is False:
                    continue

                #self.__used_words.add_word(match)

                if (self.__iterations % self.__update_frequency == 0):
                    print_crossword(self.__crossword, entries_copy)

                if self.__solve_backtracking(entries_copy):
                    return True

                # that branch didn't go well, trying next
                entry_copy.set_is_valid(False)
                entry_copy.set_value(pattern)
                #self.__used_words.remove_word(match)
                #print_crossword(self.__crossword, entries)

            return False  # backtracking
        return True


    def __forward_check(self, entry_index, entries, descend=True):
        entry = entries[entry_index]
        pattern = entry.value()

        for relation_index, relation in enumerate(entry.relations()):
            pattern_as_list = list(pattern)
            other = entries[relation.index()]
            #if other.is_valid() is True:
            #    continue

            #other_pattern_as_list = list(other.value())
            other_pattern = get_pattern(relation.index(), entries)
            other_pattern_as_list = list(other_pattern)
            pos_in_entry, pos_in_other = get_entries_intersection(relation.coordinate(), entry, other)
            other_pattern_as_list[pos_in_other] = pattern_as_list[pos_in_entry]
            other_pattern = "".join(other_pattern_as_list)
            other_matches = self.__matcher.get_matches(other_pattern)
            if len(other_matches) == 0:
                return False

        return True


    def run(self):
        self.__create_graph_x()
        labels = nx.get_node_attributes(self.__graph, 'desc')
        save_graph_to_image(self.__graph, "graph.png")

        self.__print_graph_info(self.__graph)
        print(self.__solve_backtracking(self.__crossword.entries()))


    def __print_graph_info(self, graph):
        print("is tree", nx.is_tree(graph))
        print("is forest", nx.is_forest(graph))
        print("is connected", nx.is_connected(graph))
        indipendent_set = nx.maximal_independent_set(graph)
        igraph = nx.Graph(graph)
        igraph.remove_nodes_from(indipendent_set)
        save_graph_to_image(igraph, "indipendent.png")

        mst_graph = nx.minimum_spanning_tree(nx.Graph(graph))
        save_graph_to_image(mst_graph, "minimum_spanning_tree.png")

        articulation_points = list(nx.articulation_points(graph))
        ap_graph = nx.Graph(graph)
        ap_graph.remove_nodes_from(articulation_points)
        save_graph_to_image(ap_graph, "articulation_points.png")

