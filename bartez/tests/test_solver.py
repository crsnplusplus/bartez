import unittest

from bartez.tests.test_utils import *


class TestBartezSolver(unittest.TestCase):
    def test_bartez_solver_create_graph(self):
        board, geometry = boards.get_default_board()
        _ = Crossworld(geometry[0], geometry[1])


        return
