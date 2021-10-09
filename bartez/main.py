from bartez import boards
from bartez.crossword import Crossworld
from bartez.symbols import SquareValues
from bartez.solver.solver import CrosswordSolver
from bartez.word_dictionary import Dictionary


def get_dictionary():
    return Dictionary("italian", "words.txt")


def main():
    dictionary = get_dictionary()
    print("done")
    print("words count: ", dictionary.get_words_count())
    board, geometry = boards.get_default_board()
    crossword = Crossworld(geometry[0], geometry[1])

    for p in board:
        r, c = p[0], p[1]
        crossword.set_symbol(r, c, SquareValues.block)

    crossword.prepare()
    crossword.print_crossword()

    solver = CrosswordSolver(dictionary, crossword)
    solver.run()


if __name__ == "__main__":
    main()
