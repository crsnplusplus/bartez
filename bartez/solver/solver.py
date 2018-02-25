import networkx as nx
"""from networkx.algorithms.community import *"""
from copy import copy
from bartez.utils_plot import save_graph_to_image
from bartez.utils_debug import print_crossword
from bartez.utils_solver import get_pattern, get_matches, are_there_enough_matches, get_entries_intersection


class CrosswordSolver:
    def __init__(self, dictionary=None, crossword=None):
        self.__dictionary = dictionary
        self.__crossword = crossword
        self.__graph = None
        self.__traverse_order = []

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
        print_crossword(self.__crossword, entries)

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

    def run(self):
        self.__create_graph_x()
        labels = nx.get_node_attributes(self.__graph, 'desc')
        save_graph_to_image(self.__graph, "graph.png")

        self.__print_graph_info(self.__graph)
        print(self.__solve_backtracking(self.__crossword.entries()))

    def __find_bridges(self):
        graph_order = self.get_num_of_vertex()
        bridges = []
        for vertex1 in range(graph_order):
            for vertex2 in range(graph_order):
                if vertex1 == vertex2:
                    continue
                graph = nx.Graph(self.__graph)
                graph.remove_node(vertex1)
                graph.remove_node(vertex2)
                if nx.is_biconnected(graph):
                    bridges.append([vertex1, vertex2])
        return bridges

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

        #greater_biconnected = max(nx.biconnected_components(graph), key=len)
        #greater_biconnected_graph = nx.Graph(graph)
        #cuts_and_bridges_graph = nx.Graph(graph)
        #cuts_and_bridges_graph.remove_nodes_from(greater_biconnected)
        #save_graph_to_image(cuts_and_bridges_graph, "cuts_and_bridges_graph.png")

        #from utils_solver import bridges
        #bridges = bridges(graph)
        #for u in bridges:
        #    print u

        #print list(bridges)

        #s = nx.connected_component_subgraphs(self.__graph)
        #print s
        """
        import kernighan_lin as kl
        sets = kl.kernighan_lin_bisection(graph, max_iter=50)
        for klset in sets:
            print(klset)
        
        s1graph = nx.Graph(graph)
        s1graph.remove_nodes_from(sets[0])
        save_graph_to_image(s1graph, "kernighan_lin_bisection_1.png")

        s2graph = nx.Graph(graph)
        s2graph.remove_nodes_from(sets[1])
        save_graph_to_image(s2graph, "kernighan_lin_bisection_2.png")

        s3graph = nx.Graph(graph)
        s3graph.remove_nodes_from(sets[0])
        s3graph.remove_nodes_from(sets[1])
        print(s3graph)
        print("done")
        """