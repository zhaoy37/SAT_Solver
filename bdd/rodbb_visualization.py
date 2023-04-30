"""
Authors: Ziyan An
References:

Implementation for displaying an ROBDD graph using
networkx graph struct.
"""

import plotly
import numpy as np
import networkx as nx
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from bdd.robdd_graph import ROBDD_graph

plt.rcParams['interactive']


def map_to_color(G):
    usable_colors = ['red', 'blue', 'green', 'orange', 'purple']
    ColorLegend = {'Obsolete': 2,'Initialisation': 1,'Draft': 4,'Release': 3} 
    node_var = list(G.nodes(data="var"))
    color_map = []
    print(node_var)
    for n in node_var:
        if n[0]<= 1:
            color_map.append('pink')
        else:
            color_map.append(usable_colors[n[-1]])
    return color_map

def view_rodbb(g):
    G = nx.DiGraph()
    node_id = 0
    node_map = {}
    edge_labels = {}
    for k, v in g._graph.items():
        node_map[k] = node_id
        if k.var == -1:
            G.add_nodes_from([(node_id, {'var':k.path[0][-1], 'color':'red'})])
        else:
            G.add_nodes_from([(node_id, {'var':k.var, 'color':'blue'})])
        if v: 
            G.add_edge(node_id, node_map[v[0]])
            edge_labels[(node_id, node_map[v[0]])] = 'low'
            G.add_edge(node_id, node_map[v[1]])
            edge_labels[(node_id, node_map[v[1]])] = 'high'
        node_id += 1 

    color_map = map_to_color(G)
    pos = nx.spring_layout(G, scale=20, k=3/np.sqrt(G.order()))
    labels = nx.get_node_attributes(G, 'var') 
    for k, val in labels.items():
        if k> 1:
            labels[k] = 'x'+str(val)
    nx.draw(G, pos=pos, node_size=500, with_labels=True, 
            node_color=color_map, alpha=0.6, 
            labels=labels)
    nx.draw_networkx_edge_labels(G, pos=pos, 
            edge_labels= edge_labels,
            font_color='pink')

    plt.show()
