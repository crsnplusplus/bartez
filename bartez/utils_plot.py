import networkx as nx


def save_graph_to_image(graph, path):
    """
    @todo solve pygraphviz dependency on windows
    viz = nx.nx_agraph.to_agraph(graph)
    viz.layout(prog='neato')  # prog = ['neato' | 'dot' | 'twopi' | 'circo' | 'fdp' | 'nop']
    viz.draw("_" + path, format="png")
    """