"""
Author: Yiqi (Nick) Zhao

This file is constructs an auxiliary data structure (graph) used for
the graph coloring problems. The graph is defined in the format of
adjacency list. It also provides methods for solving the graph coloring problems.
"""


# Define the class for node.
class Node:
    def __init__(self, name, connections):
        self.name = name
        self.connections = connections


# Define the class for graph.
class Graph:
    def __init__(self, colors):
        self.graph = dict()
        self.colors = dict()

    def assign_node(self, node):
        self.graph[node.name] = node.connections