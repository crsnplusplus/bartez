import unittest

import networkx as nx
from networkx.algorithms.community.kernighan_lin import kernighan_lin_bisection

from bartez import boards
from bartez import entry
from bartez.crossword import Crossworld, SquareValues
from bartez.tests.test_utils import *

class Test_bartez_graph_dev(unittest.TestCase):
    def test_bartez_graph_nx_create(self):
        crossword = get_test_crossword()
        entries = crossword.get_entries()
        graph = get_test_graph(crossword)
        self.assertTrue((len(entries)) == graph.number_of_nodes())

    def test_bartez_graph_nx_split_two(self):
        crossword = get_test_crossword()
        entries = crossword.get_entries()
        graph = get_test_graph(crossword)
        self.assertTrue((len(entries)) == graph.number_of_nodes())

        subgraphs, subsections = split_graph(graph)

        print_test_graph_info(graph, "root")
        print("subgraphs: " + str(len(subgraphs)))

        for subgraph_index, subgraph in enumerate(subgraphs):
            print_test_graph_info(subgraph, "graph.subgraph."+str(subgraph_index))

        first = subgraphs[0]
        second = subgraphs[1]
        common = find_graph_common_entries(entries, first, second)

        section_index = 0
        for section_index, subsection in enumerate(subsections):
            for entry_index in subsection:
                entry = entries[entry_index]
                entry_value = entry.get_value()
                entry_value_len = len(entry_value)

                entry_value = str(section_index + 1)*entry_value_len
                entry.set_value(entry_value)

        for c in common:
            entry = entries[c]
            entry.set_value(('+')*len(entry.get_value()))

        crossword.set_entries(entries)
        crossword.print_crossword()

        for c in common:
            entry = entries[c]
            print("common: " + entry.description())


if __name__ == '__main__':
    unittest.main()
