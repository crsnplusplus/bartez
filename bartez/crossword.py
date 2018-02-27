from __future__ import print_function
from enum import Enum
from bartez.entry import Entry, Coordinate, Orientation, Relation


class SquareValues(Enum):
    char = u'.'
    block = u'\u2588'


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
        count = directions_to_index(Direction.count)
        self.__neighbours = [None for _ in range(count)]
        self.__value = value
        self.__point = [x, y]

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

    def set_value(self, value):
        self.__value = value

    def get_value(self):
        return self.__value

    def count_squares_to_block(self, direction):
        count = 0

        current = self.__neighbours[directions_to_index(direction)]

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
        self.__grid = []
        self.__entries = []
        self.__intersections = []
        self.set_geometry(rows, columns)

    def set_geometry(self, rows, columns):
        self.__rows = rows
        self.__columns = columns
        self.__grid = [[Square() for _ in range(columns)] for _ in range(rows)]

    def set_value(self, row, column, value):
        #  print "row: ", row, " column: ", column, " value: ", value
        self.__grid[row][column] = Square(row, column, value)

    def set_value_from_entry(self, entry):
        for i, char in enumerate(list(entry.value())):
            row = entry.x() if entry.horizontal() else entry.x() + i
            col = entry.y() + i if entry.horizontal() else entry.y()
            self.__grid[row][col].set_value(char)
        return

    def get_value(self, row, column):
        return self.__grid[row][column].get_value()

    def set_blocks(self, blocks):
        for block in blocks:
            r = block[0]
            c = block[1]

            if c >= self.__columns:
                continue

            if r >= self.__rows:
                continue

            self.__grid[r][c].set_value(Square(r, c, SquareValues.block))

    def set_entries(self, entries):
        self.__entries = entries

        for entry in entries:
            value = entry.get_value()
            if str('.') in value:
                continue
            self.set_value_from_entry(entry)

    def get_entries(self):
        return self.__entries

    def clear_all_non_blocks(self):
        for square_column in self.__grid:
            for square in square_column:
                if square.is_block() is False:
                    square.set_value(SquareValues.char)

    def print_crossword(self):
        print('')

        for r in range(0, self.__rows):
            for c in range(0, self.__columns):
                char = self.__grid[r][c].get_value()
                if char == SquareValues.block:
                    """
                    @todo replace unicode value, now it produces codec ascii error
                    print('\u2588', end=' '),
                    """
                    print('#', end=' '),
                elif char == SquareValues.char:
                    print(u'.', end=' '),
                else:
                    print(char, end=' '),

            print('')

        print('')

    def __update_neighbours(self):
        for r in range(0, self.__rows):
            for c in range(0, self.__columns):
                square = self.__grid[r][c]
                up, down, right, left = None, None, None, None

                if (r > 0) and (r < self.__rows):
                    up = self.__grid[r-1][c]

                if (c >= 0) and (c < self.__columns - 1):
                    right = self.__grid[r][c+1]

                if (r >= 0) and (r < self.__rows - 1):
                    down = self.__grid[r+1][c]

                if (c > 0) and (c < self.__columns):
                    left = self.__grid[r][c-1]

                square.set_neighbours(up, down, left, right)

    def __update_entries(self):
        entries_count = 0
        for r in range(0, self.__rows):
            for c in range(0, self.__columns):
                square = self.__grid[r][c]

                if square.is_block():
                    continue

                up = square.count_squares_to_block(Direction.up)
                right = square.count_squares_to_block(Direction.right)
                down = square.count_squares_to_block(Direction.down)
                left = square.count_squares_to_block(Direction.left)

                is_vertical = (up == 0) and (down >= 1)
                is_horizontal = (left == 0) and (right >= 1)

                if is_horizontal is False and is_vertical is False:
                    continue

                entries_count += 1

                if is_horizontal is True:
                    coordinate = Coordinate(r, c)
                    orientation = Orientation.horizontal
                    length = right + 1
                    number = entries_count
                    entry = Entry(coordinate, orientation, number, length)
                    entry.set_description(str(number) + " Horizontal")
                    self.__entries.append(entry)

                if is_vertical is True:
                    coordinate = Coordinate(r, c)
                    orientation = Orientation.vertical
                    length = down + 1
                    number = entries_count
                    entry = Entry(coordinate, orientation, number, length)
                    entry.set_description(str(number) + " Vertical")
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

                if len(intersection) is 0:
                    continue

                assert(len(intersection) is 1)

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
                square = self.__grid[r][c]
                print("Square: ", r, ", ", c)
                print("  up", square.get_neighbour(Direction.up))
                print("  right", square.get_neighbour(Direction.right))
                print("  down", square.get_neighbour(Direction.down))
                print("  left", square.get_neighbour(Direction.left))

    def __print_entries(self):
        for index, entry in enumerate(self.__entries):
            print(index, ": ", entry.get_description())
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
