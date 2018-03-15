import networkx as nx
from bartez.graph.graph_node import BartezGraphNodeVisitableEntry

from copy import copy

class BartezGraph(nx.Graph):
    def __init__(self, local_entries, container_entries):
        nx.Graph.__init__(self)
        self.__local_entries = local_entries
        self.__container_entries = container_entries
        self.__populate()

    def get_local_entries(self):
        return self.__local_entries

    def __get_local_entries_as_absolute_indices(self):
        indices = [entry.absolute_index() for entry in self.__local_entries]
        return indices

    def get_container_entries(self):
        return self.__container_entries

    def __populate(self):
        local_entries_as_indices = self.__get_local_entries_as_absolute_indices()

        for entry in self.__local_entries:
            bartez_node = BartezGraphNodeVisitableEntry(entry.absolute_index(),
                                                        entry,
                                                        entry.description(),
                                                        self)
            self.add_node(entry.absolute_index(),
                          entry=entry,
                          desc=str(entry.description()),
                          bartez_node=bartez_node)

            relations = entry.relations()

            for index_relation, relation in enumerate(relations):
                relation_index = relation.index()
                if relation_index not in local_entries_as_indices:
                    continue

                self.add_edge(entry.absolute_index(), relation_index)

