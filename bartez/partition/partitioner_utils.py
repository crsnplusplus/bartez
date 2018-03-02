from bartez.partition.partition import BartezPartitionEntriesNode
import bartez.partition.partition_utils as partition_utils

from networkx.algorithms.community.kernighan_lin import kernighan_lin_bisection
import networkx as nx

from copy import copy


def partition_split(root_partition, entries):
    partitions = []
    splitted_subgraphs, _ = split_graph_kernighan_lin_bisection(root_partition.get_graph())

    for splitted_subgraph in splitted_subgraphs:

        for connected_component in nx.connected_components(splitted_subgraph):

            connected_graph = splitted_subgraph.subgraph(connected_component)
            connected_graph_entries = select_entries_from_graph(entries, connected_graph)

            partitions.append(connected_graph_entries)

    return partitions


def subpartition_with_max_vertex_count(root_partition, entries, max_vertex_count):
    partitions = []
    vertex_count = len(root_partition.get_entries())

    has_enough_vertex = vertex_count <= max_vertex_count

    if has_enough_vertex == True:
        partitions.append(root_partition)
        return partitions

    partitions_splitted = partition_split(root_partition, entries)

    for partition_splitted in partitions_splitted:
        sub_partitions = subpartition_with_max_vertex_count(BartezPartitionEntriesNode(partition_splitted),
                                                            entries,
                                                            max_vertex_count)

        for sub_partition in sub_partitions:
            partitions.append(sub_partition)

    return partitions


def select_entries_from_graph(entries, graph):
    selected_entries = []
    nodes = graph.nodes()

    for node in nodes:
        selected_entries.append(entries[node])

    return selected_entries

def partition_minimum(entries_to_partition):
    entries = copy(entries_to_partition)
    partitions = []

    while len(entries) > 0:
        partition_entries = []

        entry = entries[0]
        relations = entry.relations()
        # append entry
        partition_entries.append(entry)

        for index_relation, relation in enumerate(relations):
            relation_entry = entries_to_partition[relation.index()]
            # append entry relation too
            if relation_entry in entries:
                partition_entries.append(relation_entry)

        partition = BartezPartitionEntriesNode(partition_entries)
        partitions.append(partition)

        # remove from entries
        entries = list(filter(lambda x: x not in partition_entries, entries))

    return partitions


def split_graph_kernighan_lin_bisection(graph):
    sections = kernighan_lin_bisection(graph, max_iter=2)#max_iter=graph.number_of_nodes())
    subgraphs = []

    for section_index, section in enumerate(sections):
        subgraph = graph.subgraph(section).copy()
        subgraphs.append(subgraph)

    return subgraphs, sections