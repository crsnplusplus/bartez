import unittest

import networkx as nx
from networkx.algorithms.community.kernighan_lin import kernighan_lin_bisection

from bartez.graph.graph import BartezGraph
from bartez.crossword import Crossworld, SquareValues
from bartez.tests.test_utils import *

class Test_bartez_graph(unittest.TestCase):
    def test_bartez_graph_create(self):
        crossword = get_test_crossword()
        bartez_graph = BartezGraph(crossword)
        return

if __name__ == '__main__':
    unittest.main()

