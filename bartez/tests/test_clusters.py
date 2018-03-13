import unittest

import bartez.tests.test_utils as test_utils
from bartez.graph.cluster import BartezClusterContainer


class TestBartezCluster(unittest.TestCase):
    def test_bartez_cluster(self):
        crossword = test_utils.get_test_crossword()
        entries = crossword.get_entries()
        graph = test_utils.get_test_graph(crossword)
        container = BartezClusterContainer(entries, 4)


if __name__ == '__main__':
    unittest.main()
