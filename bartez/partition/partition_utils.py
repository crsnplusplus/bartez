import networkx as nx

def create_nx_graph_from_entries(entries):
    graph = nx.Graph()
    num_of_vertex = len(entries)

    for index_entry, entry in enumerate(entries):
        graph.add_node(index_entry, desc=str(entry.description()))
        relations = entry.relations()

        for index_relation, relation in enumerate(relations):
            graph.add_edge(index_entry, relation.index())

    traverse_order = get_traverse_order(graph)
    return graph, num_of_vertex, traverse_order


def get_traverse_order(graph):
    bfs = nx.dfs_tree(graph, 0)
    bfs_to = list(nx.dfs_preorder_nodes(bfs))
    return bfs_to


def get_all_relations_as_entries(entries):
    all_relations = []

    for entry_index, entry in enumerate(entries):
        relations = entry.relations()

        for index_relation, relation in enumerate(relations):
            relation = entries[relation.index()]
            all_relations.append(relation)

    return all_relations


def get_all_unsatisfied_relations_as_entries(entries):
    unsatisfied_relations = []

    for entry_index, entry in enumerate(entries):
        relations = entry.relations()

        for index_relation, relation in enumerate(relations):
            relation = entries[relation.index()]
            if relation not in entries:
                unsatisfied_relations.append(relation)

    return unsatisfied_relations
