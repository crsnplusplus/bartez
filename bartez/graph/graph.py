import networkx as nx
from bartez.crossword import Crossworld
from bartez.entry import Entry


class BartezGraph:
    def __init__(self, crossword=None):
        self.__crossword = crossword
        self.__graph = None
        self.__traverse_order = []

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
