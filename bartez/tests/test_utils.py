from bartez import boards
from bartez.crossword import Crossworld, SquareValues
from bartez.word_dictionary import Dictionary
from bartez.dictionary.trie_serializer import *

import networkx as nx
from networkx.algorithms.community.kernighan_lin import kernighan_lin_bisection


def get_test_dictionary_path():
    return "words.txt"


def get_test_dictionary_path_1000():
    return "words_test_1000.txt"


def get_test_dictionary():
    return Dictionary("italian", get_test_dictionary_path())


def get_test_dictionary_1000():
    return Dictionary("italian", get_test_dictionary_path_1000())


def get_serialized_trie():
    trie_loaded = bartez_trie_load_from_file("bartez_trie.btt")
    return trie_loaded

def get_test_crossword():
    board, geometry = boards.get_default_board()
    crossword = Crossworld(geometry[0], geometry[1])
    for p in board:
        r, c = p[0], p[1]
        crossword.set_value(r, c, SquareValues.block)
    crossword.prepare()
    return crossword


def get_test_graph(crossword):
    graph = nx.Graph()
    entries = crossword.entries()

    for index_entry, entry in enumerate(entries):
        graph.add_node(index_entry, desc=str(entry.description()))
        relations = entry.relations()
        for index_relation, relation in enumerate(relations):
            graph.add_edge(index_entry, relation.index())

    return graph


def print_test_subgraph_info(_, name):
    print("\n* SubGraph info: " + name + "\n")


def print_test_graph_info(graph, name):
    print("\n* Graph info: " + name + "\n")
    print("is_biconnected: " + str(nx.is_biconnected(graph)))
    print("is_bipartite: " + str(nx.is_bipartite(graph)))
    print("is_chordal: " + str(nx.is_chordal(graph)))
    print("is_connected: " + str(nx.is_connected(graph)))
    print("is_directed: " + str(nx.is_directed(graph)))
    print("is_directed_acyclic_graph: " + str(nx.is_directed_acyclic_graph(graph)))
    print("is_distance_regular: " + str(nx.is_distance_regular(graph)))
    print("is_eulerian: " + str(nx.is_eulerian(graph)))
    print("is_graphical: " + str(nx.is_graphical(graph)))
    print("\n")


def get_best_connected_subgraphs(graph, max_subgraphs):
    subgraphs, sections = kernighan_lin_bisection(graph)

    connected_graphs = []
    connected_sections = []
    for subgraph_index, subgraph in enumerate(subgraphs):
        if nx.is_connected(subgraph) or len(connected_graphs) >= max_subgraphs :
            connected_graphs.append(subgraph)
            connected_sections.append(sections[subgraph_index]) #subgraph index == sections_index
        else:
            r_subgraphs, r_sections = get_best_connected_subgraphs(subgraph, max_subgraphs/2)
            for r_subgraph_index, r_subgraph in enumerate(r_subgraphs):
                #assert(nx.is_connected(r_subgraph))
                connected_graphs.append(r_subgraph)
                connected_sections.append(r_sections[r_subgraph_index])

    return connected_graphs, connected_sections


def set_all_entries_to_value(entries, value):
    for entry in entries:
        new_value = str(value)*entry.get_length()
        entry.set_value(new_value)
    return entries


def print_sub_crossword(crossword, entries):
    crossword.set_entries(entries)
    crossword.print_crossword()
    crossword.clear_all_non_blocks()