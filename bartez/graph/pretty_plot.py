import networkx as nx
from plotly.graph_objs import *

def get_node_trace(node_colors):
    node_trace = Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=Marker(
            showscale=False,
            # colorscale options
            # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
            # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
            colorscale='RdBu',
            reversescale=False,
            color=node_colors,
            size=10,
            # colorbar=dict(
            #     thickness=15,
            #     title='Node Connections',
            #     xanchor='left',
            #     titleside='right'
            # ),
            line=dict(width=2)))
    return node_trace

def get_edge_trace():
    edge_trace = Scatter(
        x=[],
        y=[],
        line=Line(width=1,color='#888'),
        hoverinfo='none',
        mode='lines')
    return edge_trace


def pretty_plot_graph(graph, entries, color_h='rgb(255,255,255)', color_v='rgb(0,0,0)'):
    #set layout
    pos = nx.kamada_kawai_layout(graph)

    node_colors = []
    for node_index, node in enumerate(graph.nodes()):
        graph.node[node]['pos'] = pos[node]
        entry = entries[node]
        color = color_h if entry.is_horizontal() else color_v
        node_colors.append(color)

    edge_trace = get_edge_trace()
    node_trace = get_node_trace(node_colors)

    for edge in graph.edges():
        x0, y0 = graph.node[edge[0]]['pos']
        x1, y1 = graph.node[edge[1]]['pos']
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [y0, y1, None]

    for node in graph.nodes():
        x, y = graph.node[node]['pos']
        node_trace['x'].append(x)
        node_trace['y'].append(y)
        node_trace['text'].append(graph.node[node]['desc'])

    fig = Figure(data=Data([edge_trace, node_trace]),
                layout=Layout(
                title='<br>Bartez crossword graph',
                    titlefont=dict(size=22),
                    showlegend=True,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        #text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))
    return fig


def pretty_plot_subgraphs(root_graph, subgraphs):
    from random import randint

    pos = nx.kamada_kawai_layout(root_graph)
    node_colors = []

    random_color_gen = lambda : "rgb("+ str(randint(0, 255)) + "," + \
                                        str(randint(0, 255)) + "," + \
                                        str(randint(0, 255)) +")"

    for subgraph_index, subgraph in enumerate(subgraphs):
        nodes = subgraph.nodes()

        random_color = random_color_gen()

        for node_index, node in enumerate(nodes):
            subgraph.node[node]['pos'] = pos[node]
            node_colors.append(random_color)

    edge_trace = get_edge_trace()
    node_trace = get_node_trace(node_colors)

    for edge in root_graph.edges():
        x0, y0 = root_graph.node[edge[0]]['pos']
        x1, y1 = root_graph.node[edge[1]]['pos']
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [y0, y1, None]

    for node in root_graph.nodes():
        x, y = root_graph.node[node]['pos']
        node_trace['x'].append(x)
        node_trace['y'].append(y)
        node_trace['text'].append(root_graph.node[node]['desc'])

    fig = Figure(data=Data([edge_trace, node_trace]),
                layout=Layout(
                title='<br>Bartez crossword graph',
                    titlefont=dict(size=22),
                    showlegend=True,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        #text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))
    return fig
