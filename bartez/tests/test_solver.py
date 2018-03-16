import unittest

import bartez.tests.test_utils as test_utils
from bartez.graph.cluster import BartezClusterContainer
from bartez.solver.container_solver import BartezClusterContainerSolver
from bartez.solver.solver_observer import BartezSolverObserverPrintCrossword
from bartez.dictionary.trie_serializer import deserialize_pattern_matcher

class TestBartezSolver(unittest.TestCase):

    def test_bartez_solver_run(self):

        crossword = test_utils.get_test_crossword()
        container = BartezClusterContainer(crossword.get_entries(), 8)
        entries_as_dict = crossword.get_entries_as_dict()
        print_observer = BartezSolverObserverPrintCrossword(crossword)

        matcher = deserialize_pattern_matcher("matcher.dat")

        solver = BartezClusterContainerSolver(entries_as_dict, container, matcher)
        solver.register_observer(print_observer)

        solver.run()
        return


if __name__ == '__main__':
    unittest.main()
