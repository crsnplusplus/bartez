from abc import ABCMeta, abstractmethod
from copy import copy

from bartez.partition.partition import BartezPartitionEntriesNode

import bartez.partition.partitioner_utils as partitioner_utils
import bartez.partition.partition_utils as partition_utils

class BartezPartitioner(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def partition(self):
        pass


class BartezPartitionerSplitter(BartezPartitioner):
    def __init__(self, entries, max_vertex=0):
        self.__entries = entries
        self.__max_partition_vertex = len(self.__entries)/2 if max_vertex <= 0 else max_vertex

    def partition(self):
        root_partition_node = BartezPartitionEntriesNode(self.__entries)
        vertex_count = self.__max_partition_vertex
        vertex_count = vertex_count if vertex_count > 0 else len(self.__entries) / 2

        partitions = partitioner_utils.subpartition_with_max_vertex_count(root_partition_node,
                                                                          self.__entries,
                                                                          vertex_count)
        return partitions


class BartezPartitionerMinimum(BartezPartitioner):
    def __init__(self, entries):
        self.__entries = entries

    def partition(self):
        return partitioner_utils.partition_minimum(copy(self.__entries))

