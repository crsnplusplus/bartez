import unittest

from bartez.dictionary.trie import *
from bartez.dictionary.trie_node import *
from bartez.dictionary.trie_node_visitor import *
from bartez.tests.test_utils import *

class Test_bartez_solver(unittest.TestCase):
    def test_bartez_solver_create_graph(self):
        board, geometry = boards.get_default_board()
        crossword = Crossworld(geometry[0], geometry[1])


        return
