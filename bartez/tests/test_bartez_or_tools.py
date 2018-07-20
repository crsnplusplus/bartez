import unittest
import datetime

from bartez import boards
from bartez.crossword import SquareValues
from bartez.crossword import Crossworld
from create_or_dictionary import *
from ortools.constraint_solver import pywrapcp


class Test_bartez_or_tools(unittest.TestCase):
    def test_bartez_or_tools(self):

        # create crossword
        board, geometry = boards.get_default_board()
        crossword = Crossworld(geometry[0], geometry[1])

        for p in board:
            r, c = p[0], p[1]
            crossword.set_value(r, c, SquareValues.block)

        crossword.prepare()
        entries = crossword.get_entries()
        or_entries_count = len(entries)
        or_entry_max_length = get_entry_max_length(entries)
        # Create the solver
        solver = pywrapcp.Solver("Problem")

        # create the dictionary
        word_list_file = "words_test_corriere.txt"
        dictionary = load_dictionary_from_file(word_list_file)
        #shuffle_words(dictionary)
        or_dictionary, or_domain = make_dictionary_matrix(dictionary, or_entry_max_length)

        or_word_count = len(or_dictionary)

        overlapping = get_entries_overlap(crossword)
        num_overlapping = len(overlapping)

        # declare variables
        or_table_vars = {}
        for I in range(or_word_count):
            for J in range(or_entry_max_length):
                or_table_vars[(I, J)] = solver.IntVar(0, 26, "A(%i,%i)" % (I, J))

        or_flat_table_vars = [or_table_vars[(I, J)] for I in range(or_word_count) for J in range(or_entry_max_length)]
        # or_entries_var = [solver.IntVar(0, or_word_count, "E%i" % I) for I in range(or_entries_count)]
        or_entries_var = []

        for I in range(or_entries_count):
            # restrict domain to the right number of letters per word
            #domain = or_domain[or_entries_length[I]]
            print("Length " + str(entries[I].get_length()))
            domain = or_domain[entries[I].get_length()]
            constraint = solver.IntVar(domain[0], domain[1], "E%i" % I)
            or_entries_var.append(constraint)

        # constraints
        solver.Add(solver.AllDifferent(or_entries_var))

        for I in range(or_word_count):
            for J in range(or_entry_max_length):
                solver.Add(or_table_vars[(I, J)] == or_dictionary[I][J])

        for I in range(num_overlapping):
            overlapping_in_first_word = or_entries_var[overlapping[I][0]] * or_entry_max_length + overlapping[I][1]
            overlapping_in_second_word = or_entries_var[overlapping[I][2]] * or_entry_max_length + overlapping[I][3]
            solver.Add(
                solver.Element(or_flat_table_vars, overlapping_in_first_word) ==
                solver.Element(or_flat_table_vars, overlapping_in_second_word)
            )

        # solution and search
        solution = solver.Assignment()
        solution.Add(or_entries_var)

        # db: DecisionBuilder
        #db = solver.Phase(or_entries_var + or_flat_table_vars, solver.INT_VAR_SIMPLE, solver.ASSIGN_MIN_VALUE)
        db = solver.Phase(or_entries_var + or_flat_table_vars, solver.INT_VAR_SIMPLE, solver.ASSIGN_MIN_VALUE)

        solver.NewSearch(db)
        num_solutions = 0
        print("Start " + str(datetime.datetime.now()))
        while solver.NextSolution():
            #print(or_entries_var)
            #print_solution(or_table_vars, or_entries_var, or_entries_count, or_entry_max_length)
            num_solutions += 1
            print("solution " + str(num_solutions) + " found: " + str(datetime.datetime.now()))
        solver.EndSearch()

        print()
        print("num_solutions:", num_solutions)
        print("failures:", solver.Failures())
        print("branches:", solver.Branches())
        print("WallTime:", solver.WallTime())

def get_entry_max_length(entries):
    max_length = 0
    for entry in entries:
        if entry.get_length() > max_length:
            max_length = entry.get_length()
    return max_length

def get_entries_intersection(c, entry, other):
    pos_in_entry = c.x() - entry.x() if entry.vertical() else c.y() - entry.y()
    pos_in_other = c.x() - other.x() if other.vertical() else c.y() - other.y()
    return pos_in_entry, pos_in_other

def get_entries_overlap(crossword):

    entries = crossword.get_entries()
    overlapping_matrix = []

    for entry_index, entry in enumerate(entries):
        relations = entry.get_relations()

        for relation in relations:
            other_entry = entries[relation.index()]
            pos_in_entry, pos_in_other = get_entries_intersection(relation.coordinate(), entry, other_entry)
            overlapping_vector = [entry_index, pos_in_entry, relation.index(), pos_in_other]
            overlapping_vector_swapped = [ overlapping_vector[2], overlapping_vector[3],
                                           overlapping_vector[0], overlapping_vector[1] ]
            if overlapping_vector_swapped in overlapping_matrix:
                continue

            overlapping_matrix.append(overlapping_vector)

    return overlapping_matrix

def print_solution(or_table_vars, or_entries, or_entries_count, word_len):
  print("")
  print("Solution: ")
  for or_entry in range(or_entries_count):
    print("%i: (%2i)" % (or_entry + 1, or_entries[or_entry].Value()), end=" ")
    print("".join(
        ["%s" % chr(ord('A') - 1 + or_table_vars[or_entries[or_entry].Value(), ii].Value()).replace('@', '') for ii in range(word_len)]
    ))

if __name__ == '__main__':
    unittest.main()
