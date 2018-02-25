import networkx as nx

def get_traverse_order(graph):
    nodes = graph.nodes()
    node_zero = graph.nodes()[0]
    bfs = nx.dfs_tree(graph, 0)
    bfs_to = list(nx.dfs_preorder_nodes(bfs))
    return bfs_to
