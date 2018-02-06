def print_error(message):
    print("(Error) ", message)


def print_crossword(crossword, entries):
    crossword.clear_all_non_blocks()
    crossword.set_entries(entries)
    crossword.print_crossword()
