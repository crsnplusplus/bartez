def print_error(message):
    print("(Error) ", message)


def print_crossword(crossword, entries):
    crossword.clear_all_non_blocks()
    crossword.set_board_values_from_entries(entries, False)
    crossword.print_crossword()