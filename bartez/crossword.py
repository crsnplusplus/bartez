from __future__ import print_function
from enum import Enum

from bartez.entry import Entry, Coordinate, Orientation, Relation
from bartez.symbols import SquareValues

class Coordinates(Enum):
    horizontal = 0
    vertical = 1


class Direction(Enum):
    up = 0
    down = 1
    right = 2
    left = 3
    count = 4


def directions_to_index(direction):
    conversion = {
        Direction.up: 0,
        Direction.down: 1,
        Direction.right: 2,
        Direction.left: 3,
        Direction.count: 4
    }

    return conversion[direction]


class Square:
    def __init__(self, x=-1, y=-1, value=SquareValues.char):
        self.__neighbours = []
        self.__value = value
        self.__point = [x, y]
        self.__neighbours = [None for _ in range(directions_to_index(Direction.count))]

    def reset(self, x=-1, y=-1, value=SquareValues.char):
        self.__neighbours = []
        self.__value = value
        self.__point = [x, y]
        self.reset_neighbours()

    def reset_neighbours(self):
        self.__neighbours = [None for _ in range(directions_to_index(Direction.count))]

    def is_block(self):
        return self.__value == SquareValues.block

    def set_coordinates(self, coordinates):
        self.__point[0] = coordinates[0]
        self.__point[1] = coordinates[1]

    def get_coordinates(self):
        return self.__point[0]

    def set_neighbour(self, direction, neighbour):
        self.__neighbours[directions_to_index(direction)] = neighbour

    def set_neighbours(self, up, down, left, right):
        self.__neighbours[directions_to_index(Direction.up)] = up
        self.__neighbours[directions_to_index(Direction.down)] = down
        self.__neighbours[directions_to_index(Direction.left)] = left
        self.__neighbours[directions_to_index(Direction.right)] = right

    def get_neighbour(self, direction):
        d = directions_to_index(direction)
        return self.__neighbours[d]

    def has_char_neighbour_in_direction(self, direction):
        d = directions_to_index(direction)
        if self.__neighbours[d] == None:
            return False
        return self.__neighbours[d].is_block() == False

    def has_char_neighbours(self):
        has_char_neighbours = False
        has_char_neighbours |= self.has_char_neighbour_in_direction(Direction.up)
        has_char_neighbours |= self.has_char_neighbour_in_direction(Direction.down)
        has_char_neighbours |= self.has_char_neighbour_in_direction(Direction.left)
        has_char_neighbours |= self.has_char_neighbour_in_direction(Direction.right)
        return has_char_neighbours

    def set_value(self, value):
        self.__value = value

    def     get_value(self):
        return self.__value

    def count_squares_to_block(self, direction):
        assert(self.is_block() == False)

        current = self.__neighbours[directions_to_index(direction)]
        count = 0

        while current is not None:
            if current.is_block() is True:
                break

            count = count + 1
            current = current.get_neighbour(direction)

        return count


class Crossworld:
    def __init__(self, rows=0, columns=0):
        self.__rows = 0
        self.__columns = 0
        self.__board = []
        self.__entries = []
        self.__intersections = []
        self.set_geometry(rows, columns)

    def get_rows_count(self):
        return self.__rows

    def get_columns_count(self):
        return self.__columns

    def has_char_neighbours_at_square(self, x, y):
        return self.__board[x][y].has_char_neighbours()

    def has_squares_with_no_char_neighbours(self):
        return len(self.get_squares_pos_with_no_char_neighbours()) > 0

    def get_squares_pos_with_no_char_neighbours(self):
        squares = []
        for r in range(0, self.__rows):
            for c in range(0, self.__columns):
                if self.__board[r][c].is_block():
                    continue
                if self.__board[r][c].has_char_neighbours() == False:
                    squares.append([r, c])
        return squares

    def set_geometry(self, rows, columns):
        self.__rows = rows
        self.__columns = columns
        self.__board = [[Square() for _ in range(columns)] for _ in range(rows)]


    def set_symbol(self, r, c, symbol):
        #print("row: " + str(r) + " column: " + str(c) + " value: " + str(value))
        self.__board[r][c].set_value(symbol)


    def set_board_value_from_entry(self, entry):
        for i, char in enumerate(list(entry.value())):
            row = entry.x() if entry.horizontal() else entry.x() + i
            col = entry.y() + i if entry.horizontal() else entry.y()
            self.__board[row][col].set_value(char)
        return


    def get_value(self, row, column):
        return self.__board[row][column].get_value()


    def set_blocks(self, blocks):
        for block in blocks:
            r = block[0]
            c = block[1]

            if c >= self.__columns:
                continue

            if r >= self.__rows:
                continue

            self.__board[r][c].set_value(SquareValues.block)


    def update_entries_from_board_value(self, row, col, value):
        for entry in self.__entries:
            entry.set_value_from_point(row, col, value)


    def set_board_values_from_entries(self, entries, bypassEmptyCheck=False):
        self.__entries = entries

        for entry in entries:
            value = entry.get_value()
            if bypassEmptyCheck == False and str(SquareValues.char) in value:
                continue

            self.set_board_value_from_entry(entry)


    def get_entries(self):
        return self.__entries


    def get_entries_as_dict(self):
        entries_as_dict = {}
        for single_entry in self.__entries:
            entries_as_dict[single_entry.absolute_index()] = single_entry
        return entries_as_dict


    def clear_all_non_blocks(self):
        for square_column in self.__board:
            for square in square_column:
                if square.is_block() is False:
                    square.set_value(SquareValues.char)


    def get_entries_intersection(self, c, entry, other):
        pos_in_entry = c.x() - entry.x() if entry.vertical() else c.y() - entry.y()
        pos_in_other = c.x() - other.x() if other.vertical() else c.y() - other.y()
        return pos_in_entry, pos_in_other


    def apply_entry_on_relations(self, entry, pattern):
        entries = self.__entries
        entry.set_value(pattern)
        #pattern = entry.value()
        pattern_as_list = list(pattern)
        #print entry.description(), ":"
        #print "  x: ", entry.x(), ", y: ", entry.y()

        for _, relation in enumerate(entry.relations()):
            other_index = relation.index()
            other = entries[other_index]
            other_pattern = other.value()
            other_pattern_as_list = list(other_pattern)
            print("  relation with ", other.description(), ":")
            pos_in_entry, pos_in_other = self.get_entries_intersection(relation.coordinate(), entry, other)
            other_pattern_as_list[pos_in_other] = pattern_as_list[pos_in_entry]
            other_pattern_as_string = "".join(other_pattern_as_list)
            other.set_value(other_pattern_as_string)


    def print_crossword(self):
        print('')

        for r in range(0, self.__rows):
            for c in range(0, self.__columns):
                char = self.__board[r][c].get_value()
                if char == SquareValues.block:
                    print('#', end=' '),
                elif char == SquareValues.char:
                    print('.', end=' '),
                else:
                    print(char, end=' '),

            print('')

        print('')


    def __update_neighbours(self):
        for r in range(0, self.__rows):
            for c in range(0, self.__columns):
                #square = self.__grid[r][c]
                up, down, right, left = None, None, None, None

                if self.__board[r][c].is_block():
                    continue

                if (r > 0) and (r < self.__rows):
                    up = self.__board[r-1][c]

                if (c >= 0) and (c < self.__columns - 1):
                    right = self.__board[r][c+1]

                if (r >= 0) and (r < self.__rows - 1):
                    down = self.__board[r+1][c]

                if (c > 0) and (c < self.__columns):
                    left = self.__board[r][c-1]

                self.__board[r][c].set_neighbours(up, down, left, right)


    def __update_entries(self):
        entries_count = 0
        self.__entries.clear()
        for r in range(0, self.__rows):
            for c in range(0, self.__columns):
                square = self.__board[r][c]

                if square.is_block():
                    continue

                up = square.count_squares_to_block(Direction.up)
                right = square.count_squares_to_block(Direction.right)
                down = square.count_squares_to_block(Direction.down)
                left = square.count_squares_to_block(Direction.left)

                is_vertical = (up == 0) and (down >= 1)
                is_horizontal = (left == 0) and (right >= 1)

                if is_vertical is False and is_horizontal is False:
                    continue

                entries_count += 1

                if is_horizontal is True:
                    coordinate = Coordinate(r, c)
                    orientation = Orientation.horizontal
                    length = right + 1
                    number = entries_count
                    entry = Entry(coordinate, orientation, number, length)
                    entry.set_description(str(number) + " Horizontal")
                    entry.set_absolute_index(len(self.__entries))
                    self.__entries.append(entry)
                    
                if is_vertical is True:
                    coordinate = Coordinate(r, c)
                    orientation = Orientation.vertical
                    length = down + 1
                    number = entries_count
                    entry = Entry(coordinate, orientation, number, length)
                    entry.set_description(str(number) + " Vertical")
                    entry.set_absolute_index(len(self.__entries))
                    self.__entries.append(entry)

        return len(self.__entries)


    @staticmethod
    def __get_entry_domain(entry):
        if entry.horizontal():
            entry_domain = [Coordinate(entry.x(), entry.y() + i) for i in range(entry.length())]
        else:
            entry_domain = [Coordinate(entry.x() + i, entry.y()) for i in range(entry.length())]
        return entry_domain


    def __update_entries_relations(self):
        entries_count = len(self.__entries)
        intersection_matrix = [[-1 for _ in range(entries_count)] for _ in range(entries_count)]

        for index_entry, entry in enumerate(self.__entries, start=0):
            entry.remove_all_relations()
            entry_domain = self.__get_entry_domain(entry)

            for index_other, other in enumerate(self.__entries, start=0):
                if entry == other:
                    continue

                if entry.get_orientation() == other.get_orientation():
                    continue

                other_domain = self.__get_entry_domain(other)

                intersection = []
                for coordinate_e in entry_domain:
                    for coordinate_o in other_domain:
                        if coordinate_e.x() == coordinate_o.x() and coordinate_e.y() == coordinate_o.y():
                            intersection.append(coordinate_e)

                if len(intersection) == 0:
                    continue

                assert(len(intersection) == 1)

                coordinate = intersection[0]
                pos_in_entry = coordinate.x() - entry.x() if entry.horizontal() else coordinate.y() - entry.y()
                pos_in_other = coordinate.x() - other.x() if other.horizontal() else coordinate.y() - other.y()
                intersection_matrix[pos_in_entry][pos_in_other] = pos_in_entry
                relation = Relation(index_other, coordinate)
                entry.add_relation(relation)

        self.__intersections = intersection_matrix
        return


    def __get_intersection(self, index_entry, index_other):
        return self.__intersections[index_entry][index_other]


    def __print_neighbours(self):
        for r in range(0, self.__rows):
            for c in range(0, self.__columns):
                square = self.__board[r][c]
                print("Square: ", r, ", ", c)
                print("  up", square.get_neighbour(Direction.up))
                print("  right", square.get_neighbour(Direction.right))
                print("  down", square.get_neighbour(Direction.down))
                print("  left", square.get_neighbour(Direction.left))


    def __print_entries(self):
        for _, e in enumerate(self.__entries):
            value = e.get_value().replace("@", ".")
            desc = e.get_description() 
            desc = desc + "  " if e.is_vertical() else desc
            coordinate = e.get_coordinate()
            coordinate_str = str(coordinate.x()) + ", " + str(coordinate.y())
            coordinate_end = e.get_coordinate_end()
            coordinate_end_str = str(coordinate_end.x()) + ", " + str(coordinate_end.y())
            print(str(e.absolute_index()) + 
                    ": " + desc + 
                    " [" + value + "]" +  
                    " r,c: [" + coordinate_str +"] -> " + 
                    "[" + coordinate_end_str +"]"
            )
        return


    def __print_entries_relations(self):
        return


    def prepare(self):
        self.__update_neighbours()
        self.__update_entries()
        self.__update_entries_relations()
        return


    def print_info(self):
        #print "*** Neighbours ***"
        #self.__print_neighbours()

        print("*** Entries ***")
        self.__print_entries()

    entries = get_entries
    get_intersection = __get_intersection
