import unittest

from bartez.tests.test_utils import *

import bartez.graph as btz
from bartez.graph.graph import BartezGraph

import bartez.graph.graph_utils as graph_utils

def prepare_sub_entries(entries, graph, value):
    entries_from_graph = btz.graph_utils.extract_entries_from_graph(entries, graph)
    return set_all_entries_to_value(entries_from_graph, value)


class TestBartezGraph(unittest.TestCase):
    def test_bartez_graph_create(self):
        crossword = get_test_crossword()
        bartez_graph = BartezGraph(crossword)
        return


    def test_bartez_graph_split2(self):
        crossword = get_test_crossword()
        entries = crossword.get_entries()
        bartez_graph = BartezGraph(crossword)
        nx_graph = bartez_graph.get_nx_graph()

        g1, g2, gi = btz.graph_utils.split_graph_with_frontiers(entries, nx_graph)

        gi_disconnected = btz.graph_utils.split_non_connected_sub_graphs(gi)

        #subgraphs12, sections12 = graph_utils.split_graph_connected(nx_graph)
        #self.assertTrue(len(subgraphs12) == 2)
        #self.assertTrue(len(sections12) == 2)

        crossword.print_crossword()
        crossword.clear_all_non_blocks()

        test_entries1 = prepare_sub_entries(entries, g1, u'A')
        print_sub_crossword(crossword, test_entries1)

        test_entries2 = prepare_sub_entries(entries, g2, u'B')
        print_sub_crossword(crossword, test_entries2)

        test_entriesi = prepare_sub_entries(entries, gi, u'0')
        print_sub_crossword(crossword, test_entriesi)

        crossword.clear_all_non_blocks()
        crossword.set_entries(test_entries1)
        crossword.set_entries(test_entries2)
        crossword.set_entries(test_entriesi)
        crossword.clear_all_non_blocks()

        test_entries1 = prepare_sub_entries(entries, g1, u'A')
        print_sub_crossword(crossword, test_entries1)

        test_entries2 = prepare_sub_entries(entries, g2, u'B')
        print_sub_crossword(crossword, test_entries2)

        test_entriesi = prepare_sub_entries(entries, gi, u'0')
        print_sub_crossword(crossword, test_entriesi)
        crossword.clear_all_non_blocks()

        for i, g in enumerate(gi_disconnected):
            gi_entries = prepare_sub_entries(entries, g, str(i))
            print_sub_crossword(crossword, gi_entries)

        crossword.set_entries(test_entries1)
        crossword.set_entries(test_entries2)

        for i, g in enumerate(gi_disconnected):
            gi_entries = prepare_sub_entries(entries, g, str(i))
            crossword.set_entries(gi_entries)

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
        test_entriesA = prepare_sub_entries(entries, subgraphs[0], u'A')
        print_sub_crossword(crossword, test_entriesA)

        # B = 3, 4
        test_entriesB = prepare_sub_entries(entries, subgraphs[1], u'B')
        print_sub_crossword(crossword, test_entriesB)

        # 1
        test_entries1 = prepare_sub_entries(entries, subgraphs12[0], u'1')
        print_sub_crossword(crossword, test_entries1)

        # 2
        test_entries2 = prepare_sub_entries(entries, subgraphs12[1], u'2')
        print_sub_crossword(crossword, test_entries2)

        # 3
        test_entries3 = prepare_sub_entries(entries, subgraphs34[0], u'3')
        print_sub_crossword(crossword, test_entries3)

        # 4
        test_entries4 = prepare_sub_entries(entries, subgraphs34[1], u'4')
        print_sub_crossword(crossword, test_entries4)

        crossword.set_entries(test_entries1)
        crossword.set_entries(test_entries2)
        crossword.set_entries(test_entries3)
        crossword.set_entries(test_entries4)
        crossword.print_crossword()


if __name__ == '__main__':
    unittest.main()
