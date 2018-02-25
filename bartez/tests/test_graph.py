import unittest

from copy import copy

import networkx as nx
from networkx.algorithms.community.kernighan_lin import kernighan_lin_bisection

from bartez.tests.test_utils import *
from bartez.graph.graph import BartezGraph
from bartez.crossword import Crossworld, SquareValues

import bartez.graph.graph_utils as graph_utils


class Test_bartez_graph(unittest.TestCase):
    def test_bartez_graph_create(self):
        crossword = get_test_crossword()
        bartez_graph = BartezGraph(crossword)
        return


    def test_bartez_graph_split2(self):
        crossword = get_test_crossword()
        entries = crossword.get_entries()
        bartez_graph = BartezGraph(crossword)
        nx_graph = bartez_graph.get_nx_graph()
        subgraphs12, sections12 = graph_utils.split_graph_connected(nx_graph)
        self.assertTrue(len(subgraphs12) == 2)
        self.assertTrue(len(sections12) == 2)

        crossword.print_crossword()
        crossword.clear_all_non_blocks()

        test_entries1 = graph_utils.extract_entries_from_graph(entries, subgraphs12[0])
        test_entries1 = set_all_entries_to_value(test_entries1, u'1')
        crossword.set_entries(test_entries1)
        crossword.print_crossword()
        crossword.clear_all_non_blocks()

        test_entries2 = graph_utils.extract_entries_from_graph(entries, subgraphs12[1])
        test_entries2 = set_all_entries_to_value(test_entries2, u'2')
        crossword.set_entries(test_entries2)
        crossword.print_crossword()
        crossword.clear_all_non_blocks()

        crossword.set_entries(test_entries1)
        crossword.set_entries(test_entries2)
        crossword.print_crossword()
        return


    def test_bartez_graph_split4(self):
        crossword = get_test_crossword()
        entries = crossword.get_entries()
        bartez_graph = BartezGraph(crossword)
        nx_graph = bartez_graph.get_nx_graph()
        subgraphs, sections = graph_utils.split_graph_connected(nx_graph)
        self.assertTrue(len(subgraphs) == 2)
        self.assertTrue(len(sections) == 2)

        subgraphs12, sections12 = graph_utils.split_graph_connected(subgraphs[0])
        self.assertTrue(len(subgraphs12) == 2)
        self.assertTrue(len(sections12) == 2)
        subgraphs34, sections34 = graph_utils.split_graph_connected(subgraphs[1])
        self.assertTrue(len(subgraphs34) == 2)
        self.assertTrue(len(sections34) == 2)

        crossword.print_crossword()
        crossword.clear_all_non_blocks()

        # A = 1, 2
        test_entriesA = graph_utils.extract_entries_from_graph(entries, subgraphs[0])
        test_entriesA = set_all_entries_to_value(test_entriesA, u'A')
        crossword.set_entries(test_entriesA)
        crossword.print_crossword()
        crossword.clear_all_non_blocks()

        # B = 3, 4
        test_entriesB = graph_utils.extract_entries_from_graph(entries, subgraphs[1])
        test_entriesB = set_all_entries_to_value(test_entriesB, u'B')
        crossword.set_entries(test_entriesB)
        crossword.print_crossword()
        crossword.clear_all_non_blocks()

        # 1
        test_entries1 = graph_utils.extract_entries_from_graph(entries, subgraphs12[0])
        test_entries1 = set_all_entries_to_value(test_entries1, u'1')
        crossword.set_entries(test_entries1)
        crossword.print_crossword()
        crossword.clear_all_non_blocks()

        # 2
        test_entries2 = graph_utils.extract_entries_from_graph(entries, subgraphs12[1])
        test_entries2 = set_all_entries_to_value(test_entries2, u'2')
        crossword.set_entries(test_entries2)
        crossword.print_crossword()
        crossword.clear_all_non_blocks()

        # 3
        test_entries3 = graph_utils.extract_entries_from_graph(entries, subgraphs34[0])
        test_entries3 = set_all_entries_to_value(test_entries3, u'3')
        crossword.set_entries(test_entries3)
        crossword.print_crossword()
        crossword.clear_all_non_blocks()

        # 4
        test_entries4 = graph_utils.extract_entries_from_graph(entries, subgraphs34[1])
        test_entries4 = set_all_entries_to_value(test_entries4, u'4')
        crossword.set_entries(test_entries4)
        crossword.print_crossword()
        crossword.clear_all_non_blocks()

        crossword.set_entries(test_entries1)
        crossword.set_entries(test_entries2)
        crossword.set_entries(test_entries3)
        crossword.set_entries(test_entries4)
        crossword.print_crossword()


if __name__ == '__main__':
    unittest.main()

