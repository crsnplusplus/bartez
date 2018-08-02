from enum import Enum

from operator import methodcaller

def get_entries_by_length(entries):
    return sorted(entries, key=methodcaller('get_length'), reverse=True)

def get_relations_as_entries(entry, entries):
    return [entries[r.index()] for r in entry.relations()]


def get_entries_intersection(c, entry, other):
    pos_in_entry = c.x() - entry.x() if entry.vertical() else c.y() - entry.y()
    pos_in_other = c.x() - other.x() if other.vertical() else c.y() - other.y()
    return pos_in_entry, pos_in_other


def get_pattern(entry_index, entries):
    entry = entries[entry_index]
    pattern = entry.value()
    pattern_as_list = list(pattern)
    #print entry.description(), ":"
    #print "  x: ", entry.x(), ", y: ", entry.y()
    for relation_index, relation in enumerate(entry.relations()):
        other_index = relation.index()
        other = entries[other_index]
        other_pattern = other.value()
        other_pattern_as_list = list(other_pattern)
        #print "  relation with ", other.description(), ":"
        pos_in_entry, pos_in_other = get_entries_intersection(relation.coordinate(), entry, other)
        char_other = other_pattern_as_list[pos_in_other]
        pattern_as_list[pos_in_entry] = char_other

    pattern_as_string = "".join(pattern_as_list)
    return pattern_as_string


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
        self.__value = '.' * length
        self.__relations = []
        self.__description = ""
        self.__absolute_index = -1

    def set_coordinate(self, coordinate):
        self.__coordinate = coordinate

    def get_coordinate(self):
        return self.__coordinate

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

    def get_intersection_with(self, coordinate, other):
        return get_entries_intersection(coordinate, self, other)

    def get_pattern(self, entries):
        return get_pattern(self.__absolute_index, entries)

    def get_relations_entries(self, entries):
        return get_relations_as_entries(self, entries)

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
