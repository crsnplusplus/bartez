from abc import ABCMeta, abstractmethod
from copy import copy

import bartez.partition.partitioner_utils as partitioner_utils


class BartezPartitioner(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def partition(self):
        pass


class BartezPartitionerSplitter(BartezPartitioner):
    def __init__(self, entries):
        self.__entries = entries

    def partition(self):
        return partitioner_utils.partition_split(copy(self.__entries))


class BartezPartitionerMinimum(BartezPartitioner):
    def __init__(self, entries):
        self.__entries = entries

    def partition(self):
        return partitioner_utils.partition_minimum(copy(self.__entries))

