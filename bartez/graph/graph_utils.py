from networkx.algorithms.community.kernighan_lin import kernighan_lin_bisection

import networkx as nx

def extract_entries_from_graph(entries, graph):
    extracted_entries = []
    nodes = graph.nodes()

    for n in nodes:
        extracted_entries.append(entries[n])
    return extracted_entries


def get_traverse_order(graph):
    nodes = graph.nodes()
    node_zero = graph.nodes()[0]
    bfs = nx.dfs_tree(graph, 0)
    bfs_to = list(nx.dfs_preorder_nodes(bfs))
    return bfs_to


def split_graph(graph):
    sections = kernighan_lin_bisection(graph, max_iter=2)#max_iter=graph.number_of_nodes())
    subgraphs = []

    for section_index, section in enumerate(sections):
        subgraph = graph.subgraph(section).copy()
        subgraphs.append(subgraph)

    return subgraphs, sections


def split_graph_connected(graph, max_retry=100):
    everything_is_connected = False

    dirk_gently = 0

    while everything_is_connected == False:
        dirk_gently += 1
        subgraphs, sections = split_graph(graph)

        everything_is_connected = True
        for section_index, section in enumerate(sections):
            subgraph = graph.subgraph(section).copy()
            everything_is_connected &= nx.is_connected(subgraph)

        if everything_is_connected == True:
            print("+++ retries: " + str(dirk_gently))
            return subgraphs, sections

        if dirk_gently >= max_retry:
            break

    print("+++ retries done (max and failed): " + str(dirk_gently))
    assert(False) # @todo remove assert
    return None, None
