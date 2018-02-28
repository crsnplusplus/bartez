import unittest

from bartez.tests.test_utils import *
from bartez.partition.partitioner import BartezPartitionerSplitter

class TestBartezPartitioner(unittest.TestCase):
    def test_bartez_partitioner(self):
        crossword = get_test_crossword()
        entries = crossword.get_entries()
        partitioner = BartezPartitionerSplitter(entries)
        partitions = partitioner.partition()

        for partition_index, partition in enumerate(partitions):
            entries = partition.get_entries()
            print("\nPartition " + str(partition_index) + " of " + str(len(partitions)))

            for entry in entries:
                print(entry.description())

        for partition_index, partition in enumerate(partitions):
            entries = partition.get_entries()
            entries = set_all_entries_to_value(entries, str(partition_index))
            print_sub_crossword(crossword, entries)

        for partition_index, partition in enumerate(partitions):
            entries = partition.get_entries()
            entries = set_all_entries_to_value(entries, str(partition_index))
            crossword.set_entries(entries)
        crossword.print_crossword()

        return

if __name__ == '__main__':
    unittest.main()
