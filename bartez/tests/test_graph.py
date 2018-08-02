import unittest
from copy import copy

import networkx as nx
import plotly.offline as py
from networkx.algorithms.community.kernighan_lin import kernighan_lin_bisection

import bartez.tests.test_utils as test_utils
from bartez.graph.pretty_plot import pretty_plot_graph


class TestBartezGraph(unittest.TestCase):
    def test_bartez_graph_create(self):
        crossword = test_utils.get_test_crossword()
        entries = crossword.get_entries()
        graph = test_utils.get_test_graph(crossword)
        #pp = pretty_plot_graph(graph, entries)
        #py.iplot(pp)

        sections = kernighan_lin_bisection(graph, max_iter=2)#max_iter=graph.number_of_nodes())
        subgraphs = []

        for section_index, section in enumerate(sections):
            subgraph = graph.subgraph(section)

            if nx.is_connected(subgraph):
                subgraphs.append(graph.subgraph(subgraph))
            else:
                for c in nx.connected_components(subgraph):
                    subgraphs.append(subgraph.subgraph(c))

        print(len(subgraphs))
        #pp = pretty_plot_graph(copy(subgraphs[0]), entries)
        #py.iplot(pp)


if __name__ == '__main__':
    unittest.main()
