import networkx as nx


class BartezGraph(nx.Graph):
    def __init__(self, entries):
        nx.Graph.__init__(self)
        self.__entries = entries
        self.__populate()

    def __populate(self):
        for index_entry, entry in enumerate(self.__entries):

            self.add_node(index_entry, entry=entry, desc=str(entry.description()))

            relations = entry.relations()

            for index_relation, relation in enumerate(relations):
                relation_index = relation.index()
                self.add_edge(index_entry, relation_index)

    def get_entries(self):
        return self.__entries

    def to_edge_matrix(self):
        # Initialize edge matrix
        edge_mat = [[0 for _ in range(len(self))] for _ in range(len(self))]

        # For loop to set 0 or 1 ( diagonal elements are set to 1)
        for node in self:
            tmp_neighbor_list = self.neighbors(node)

            for neighbor in tmp_neighbor_list:
                edge_mat[node][neighbor] = 1
                edge_mat[node][node] = 1

        return edge_mat
