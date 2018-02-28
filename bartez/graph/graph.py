import bartez.graph.graph_utils as graph_utils


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
        entries = self.__crossword.entries()

        g, v, to = graph_utils.create_nx_graph_from_entries(entries)

        self.__graph = g
        self.__num_of_vertex = v
        self.__traverse_order = to
