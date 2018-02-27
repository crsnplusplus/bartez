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


def split_graph_kernighan_lin_bisection(graph):
    sections = kernighan_lin_bisection(graph, max_iter=2)#max_iter=graph.number_of_nodes())
    subgraphs = []

    for section_index, section in enumerate(sections):
        subgraph = graph.subgraph(section).copy()
        subgraphs.append(subgraph)

    return subgraphs, sections


def split_graph_connected(graph, max_retry=100):
    # @todo check if input graph is connected,
    # otherwise, choose a strategy

    everything_is_connected = False
    dirk_gently = 0

    while everything_is_connected == False:
        dirk_gently += 1
        subgraphs, sections = split_graph_kernighan_lin_bisection(graph)

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


def get_graph_intersection_nodes_from_entries(entries, graph1, graph2):
    intersection_nodes = []
    for n1 in graph1.nodes():
        entry = entries[n1]
        relations = entry.get_relations()

        for r1 in relations:
            r1_index = r1.get_index()
            r1_entry = entries[r1_index]

            for n2 in graph2:
                if n2 == r1_index:
                    intersection_nodes.append(n2)

    return intersection_nodes


def get_graphs_without_intersection(entries, graph1, graph2):
    intersection_nodes = get_graph_intersection_nodes_from_entries(entries, graph1, graph2)

    graph1_without_intersection = graph1.copy()
    graph2_without_intersection = graph1.copy()

    for node in intersection_nodes:
        if graph1_without_intersection.has_node(node):
            graph1_without_intersection.remove_node(node)

    for node in intersection_nodes:
        if graph2_without_intersection.has_node(node):
            graph2_without_intersection.remove_node(node)

    return graph1_without_intersection, graph2_without_intersection, intersection_nodes


def split_graph_with_frontiers(entries, graph):
    subgraphs01, sections01 = split_graph_connected(graph)
    graph1 = subgraphs01[0].copy()
    graph2 = subgraphs01[1].copy()
    
    intersection_nodes = get_graph_intersection_nodes_from_entries(entries, graph1, graph2)
    gi = graph.subgraph(intersection_nodes).copy()

    # intersection
    #g1, g2, _ = get_graphs_without_intersection(entries, graph1, graph2)
    return graph1, graph2, gi
