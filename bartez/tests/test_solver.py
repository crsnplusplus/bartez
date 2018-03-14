import unittest

import bartez.tests.test_utils as test_utils
from bartez.graph.cluster import BartezClusterContainer
from bartez.solver.container_solver import BartezClusterContainerSolver

class TestBartezSolver(unittest.TestCase):
    def test_bartez_solver_create_graph(self):
        crossword = test_utils.get_test_crossword()
        entries = crossword.get_entries()
        dictionary = test_utils.get_serialized_trie()
        #dictionary = BartezTrie('italian', test_utils.get_test_dictionary_path_1000())
        #dictionary = test_utils.get_test_dictionary()
        container = BartezClusterContainer(entries, 8)
        solver = BartezClusterContainerSolver(dictionary, crossword, container)
        solver.run()
        return
