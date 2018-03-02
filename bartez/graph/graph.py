import networkx as nx
from networkx.algorithms.community.kernighan_lin import kernighan_lin_bisection

class BartezGraph(nx.Graph):
    def __init__(self, entries):
        nx.Graph.__init__(self)
        self.__entries = entries
        self.__populate()

    def __populate(self):
        for index_entry, entry in enumerate(self.__entries):
            self.add_node(index_entry, desc=str(entry.description()))
            relations = entry.relations()

            for index_relation, relation in enumerate(relations):
                self.add_edge(index_entry, relation.index())

    def get_entries(self):
        return self.__entries

    def split_graph_kernighan_lin_bisection(self, graph):
        sections = kernighan_lin_bisection(graph, max_iter=2)#max_iter=graph.number_of_nodes())
        subgraphs = []

        for section_index, section in enumerate(sections):
            subgraph = graph.subgraph(section).copy()
            if nx.is_connected(subgraph):
                subgraphs.append(subgraph)
            else:
                for c in nx.connected_components(subgraph):
                    subgraphs.append(graph.subgraph(c).copy())

        return subgraphs

