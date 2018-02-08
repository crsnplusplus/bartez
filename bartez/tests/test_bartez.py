import unittest

from bartez import boards
from bartez.crossword import Crossworld
from bartez.crossword import SquareValues
from bartez.solver import CrosswordSolver
from bartez.word_dictionary import Dictionary


def get_dictionary():
    return Dictionary("italian", "words.txt")


class Test_bartez(unittest.TestCase):
    def test_bartez_dictionary(self):
        dictionary = get_dictionary()
        self.assertTrue(dictionary.get_page_count() > 0)
        self.assertTrue(dictionary.get_words_count() > 0)
        self.assertTrue(len(dictionary.get_language()) > 0)

        """
    def test_bartez_solve(self):
        dictionary = get_dictionary()
        print("done")
        print("words count: ", dictionary.get_words_count())
        board, geometry = boards.get_default_board()
        crossword = Crossworld(geometry[0], geometry[1])

        for p in board:
            r, c = p[0], p[1]
            crossword.set_value(r, c, SquareValues.block)

        crossword.prepare()
        crossword.print_crossword()

        solver = CrosswordSolver(dictionary, crossword)
        solver.run()
        """

if __name__ == '__main__':
    unittest.main()