import networkx as nx

import bartez.graph.graph_utils as graph_utils
from bartez.crossword import Crossworld
from bartez.entry import Entry


class BartezGraph:
    def __init__(self, crossword=None):
        self.__crossword = crossword
        self.__graph = None
        self.__traverse_order = []
        self.__create()

    def get_nx_graph(self):
        return self.__graph.copy()

    def get_traverse_order(self):
        return self.__traverse_order

    def get_crossword(self):
        return self.__crossword

    def get_entries(self):
        return self.__crossword.entries()

    def __create(self):
        graph = nx.Graph()
        entries = self.__crossword.entries()
        self.__num_of_vertex = len(entries)

        for index_entry, entry in enumerate(entries):
            graph.add_node(index_entry, desc=str(entry.description()))
            relations = entry.relations()
            for index_relation, relation in enumerate(relations):
                graph.add_edge(index_entry, relation.index())

        self.__graph = graph
        self.__traverse_order = graph_utils.get_traverse_order(graph)
