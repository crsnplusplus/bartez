from bartez.symbols import SquareValues


def get_board_preset_01():
    board_as_string = (\
    ". . . . # . . . . . . . # . . . . . \n"
    ". . . . . . . . . # . # . . . . . . \n"
    ". . # . . . . . # . . . . . . . # . \n"
    ". # . . . . . # . . . . . . . # . . \n"
    "# . . . . . # . . . . . . . # . . . \n"
    ". . . . . # . . . . . . . # . . . . \n"
    ". . . . # . . . . . . . # . . . . . \n"
    ". . . # . . . . . . . # . . . . . # \n"
    ". . # . . . . . . . # . . . . . # . \n"
    ". # . . . . . . . # . . . . . # . . \n"
    ". . . . . . # . # . . . . . . . . . \n"
    ". . . . . # . . . . . . . # . . . . \n")
    return board_as_string

def get_board_preset_02():
    board_as_string = (\
    "0. . . # . . . . # . . . . . \n"
    ". . . . # . . . . # . . . . . \n"
    ". . . . # . . . . # . . . . . \n"
    ". . . # . . . . # . . . . . # \n"
    ". . . # . . . . . . . # # # # \n"
    "# . . . . . # # . . . . . . . \n"
    "# # . . . . . . . # . . . . . \n"
    ". . . . # . . . . . # . . . . \n"
    ". . . . . # . . . . . . . # # \n"
    ". . . . . . . # # . . . . . # \n"
    "# # # # . . . . . . . # . . . \n"
    "# . . . . . # . . . . # . . . \n"
    ". . . . . # . . . . # . . . . \n"
    ". . . . . # . . . . # . . . . \n"
    ". . . . . # . . . . # . . . . \n")
    return board_as_string


def get_board_preset_03():
    board_as_string = (\
    "# . . . . . . . . . . . . . # \n"
    ". # . . . . . . . . . . . # . \n"
    ". . # . . . . . . . . . # . . \n"
    ". . . # . . . . . . . # . . . \n"
    ". . . . # . . . . . # . . . . \n"
    ". . . . . # . . . # . . . . . \n"
    ". . . . . . # . # . . . . . . \n"
    ". . . . . . . . . . . . . . . \n"
    ". . . . . . # . # . . . . . . \n"
    ". . . . . # . . . # . . . . . \n"
    ". . . . # . . . . . # . . . . \n"
    ". . . # . . . . . . . # . . . \n"
    ". . # . . . . . . . . . # . . \n"
    ". # . . . . . . . . . . . # . \n"
    "# . . . . . . . . . . . . . # \n")
    return board_as_string

def get_board_preset_small_01():
    board_as_string=(\
        "0 1 2 \n"
        "0 # 2 \n"
        "0 1 2 \n")
    return board_as_string


def generate_board_from_string(board_as_string, block_symbol='#'):
    points = []
    
    board = board_as_string.replace(" ", "")
    strlen = len(board)
    rows = board.count("\n")
    cols = int((strlen - rows) / rows)
    board = board_as_string.replace("\n", "") \
                           .replace("\r", "") \
                           .replace(" ", "")
    assert(strlen % rows == 0)
    for i, ch in enumerate(board):
        row = int(i / cols)
        col = i % cols

        if ch == block_symbol:
            points.append([row, col])
    
    return points, [rows, cols]


def get_default_board():
    points = []
    return generate_board_from_string(get_board_preset_01())


def get_board3x3():
    return generate_board_from_string(get_board_preset_small_01())
