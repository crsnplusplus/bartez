from enum import Enum

from bartez.symbols import SquareValues


class Orientation(Enum):
    horizontal = 0
    vertical = 1


class Coordinate:
    def __init__(self, x=-1, y=-1):
        self._x = x
        self._y = y

    def x(self):
        return self._x

    def y(self):
        return self._y


class Relation:
    def __init__(self, entry_index=0, coordinate=Coordinate()):
        self.__entry_index = entry_index
        self.__coordinate = coordinate

    def get_index(self):
        return self.__entry_index

    def get_coordinate(self):
        return self.__coordinate

    def get_coordinate_x(self):
        return self.__coordinate.x()

    def get_coordinate_y(self):
        return self.__coordinate.y()

    index = get_index
    coordinate = get_coordinate
    x = get_coordinate_x
    y = get_coordinate_y


class Entry:
    def __init__(self, coordinate=Coordinate(), orientation=Orientation.horizontal, number=0, length=0):
        self.__coordinate = coordinate
        self.__orientation = orientation
        self.__number = number
        self.__length = length
        self.__is_valid = False
        self.__value = SquareValues.char * length
        self.__relations = []
        self.__description = ""
        self.__absolute_index = -1

    def set_coordinate(self, coordinate):
        self.__coordinate = coordinate

    def get_coordinate(self):
        return self.__coordinate

    def contains_point(self, px, py):
        desc = self.get_description()
        ish = self.is_horizontal()
        x_start = self.get_coordinate_x()
        x_end = (x_start + self.__length - 1) if self.is_horizontal() else x_start
        y_start = self.get_coordinate_y()
        y_end = (y_start + self.__length - 1) if self.is_vertical() else y_start
        contained =  (px >= x_start) and (px <= x_end)
        contained &= (py >= y_start) and (py <= y_end)
        return contained

    def set_value_from_point(self, px, py, value):
        if self.contains_point(px, py) == False:
            return

        ex = self.get_coordinate_x()
        ey = self.get_coordinate_y()

        ish = self.is_horizontal()

        pattern_index = px - ex if self.is_horizontal() else py - ey
        pattern = list(self.get_value())
        pattern[pattern_index] = value
        string = ''.join(str(ch) for ch in pattern)
        self.set_value(string)


    def get_coordinate_x(self):
        return self.__coordinate.x()

    def get_coordinate_y(self):
        return self.__coordinate.y()

    def set_orientation(self, orientation):
        self.__orientation = orientation

    def get_orientation(self):
        return self.__orientation

    def is_horizontal(self):
        return self.__orientation == Orientation.horizontal

    def is_vertical(self):
        return self.__orientation == Orientation.vertical

    def set_number(self, number):
        self.__number = number

    def get_number(self):
        return self.__number

    def set_length(self, length):
        self.__length = length

    def get_length(self):
        return self.__length

    def set_is_valid(self, is_valid):
        self.__is_valid = is_valid

    def is_valid(self):
        return self.__is_valid

    def set_value(self, value):
        self.__value = value

    def get_value(self):
        return self.__value

    def set_description(self, description):
        self.__description = description

    def get_description(self):
        return self.__description

    def set_relations(self, relations):
        self.__relations = relations

    def get_relations(self):
        return self.__relations

    def remove_all_relations(self):
        self.__relations = []

    def add_relation(self, relation):
        self.__relations.append(relation)

    def set_absolute_index(self, index):
        self.__absolute_index = index

    def get_absolute_index(self):
        return self.__absolute_index

    coordinate = get_coordinate
    relations = get_relations
    x = get_coordinate_x
    y = get_coordinate_y
    orientation = get_orientation
    horizontal = is_horizontal
    vertical = is_vertical
    number = get_number
    length = get_length
    valid = is_valid
    value = get_value
    description = get_description
    absolute_index = get_absolute_index
