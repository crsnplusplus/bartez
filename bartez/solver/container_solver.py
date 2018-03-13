import networkx as nx

from bartez.dictionary.trie import *
from bartez.dictionary.trie_node_visitor import *
from bartez.solver.cluster_solver import *


class BartezClusterContainerSolver:
    def __init__(self, dictionary=None, crossword=None, container=None):
        self.__dictionary = dictionary
        self.__crossword = crossword
        self.__container = container
        self.__traverse_order = []

    def set_dictionary(self, dictionary):
        self.__dictionary = dictionary

    def set_crossword(self, crossword):
        self.__crossword = crossword

    def set_container(self, container):
        self.__container = container

    def __get_first_cluster(self):
        entries = self.__crossword.entries()
        container_index = self.__container.find_entry(entries[0])
        return container_index

    def __get_container_traverse_order(self, start):
        bfs = nx.dfs_tree(self.__container, start)
        traverse_order = list(reversed(list(nx.dfs_preorder_nodes(bfs))))
        return traverse_order

    def run(self):
        first_cluster = self.__get_first_cluster()
        self.__traverse_order = self.__get_container_traverse_order(first_cluster)

        self.__solve_backtracking(self.__crossword.entries())

    def __solve_backtracking(self, entries):
        traverse_order = self.__traverse_order
        container = self.__container

        for bartez_cluster_index in traverse_order:
            bartez_cluster = container.nodes[bartez_cluster_index]

            bartez_cluster_node = bartez_cluster['cluster_bartez']
            bartez_cluster_node_graph = bartez_cluster['cluster_graph']

#            if bartez_cluster_node.is_solved():
#                continue

            cluster_entries = bartez_cluster_node.get_entries()
            solver = BartezClusterSolver(self.__dictionary, cluster_entries, bartez_cluster_node_graph)
            solver.run()

        return True

