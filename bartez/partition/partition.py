from abc import ABCMeta, abstractmethod

import bartez.partition.partition_utils as partition_utils


class BartezPartitionNode(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_entries(self):
        pass

    @abstractmethod
    def get_graph(self):
        pass


class BartezPartitionEntriesNode(BartezPartitionNode):
    def __init__(self, entries):
        self.__entries = entries
        self.__graph, _, _ = partition_utils.create_nx_graph_from_entries(entries)

    def get_entries(self):
        return self.__entries

    def get_graph(self):
        return self.__graph

    def get_unsatisfied_relations_as_entries(self):
        return partition_utils.get_all_unsatisfied_relations_as_entries(self.__entries)
