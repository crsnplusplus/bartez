import networkx as nx
from plotly.graph_objs import *

def pretty_plot_graph(graph, entries, color_h='rgb(255,255,255)', color_v='rgb(0,0,0)'):
    G = graph.copy()
    #set layout
    pos = nx.kamada_kawai_layout(graph)

    node_colors = []
    for node_index, node in enumerate(G.nodes()):
        G.node[node]['pos'] = pos[node]
        entry = entries[node]
        color = color_h if entry.is_horizontal() else color_v
        node_colors.append(color)

    edge_trace = Scatter(
        x=[],
        y=[],
        line=Line(width=1,color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in G.edges():
        x0, y0 = G.node[edge[0]]['pos']
        x1, y1 = G.node[edge[1]]['pos']
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [y0, y1, None]

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

    for node in G.nodes():
        x, y = G.node[node]['pos']
        node_trace['x'].append(x)
        node_trace['y'].append(y)
        node_trace['text'].append(G.node[node]['desc'])

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
