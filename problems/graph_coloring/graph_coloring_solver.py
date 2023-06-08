"""
Author: Yiqi (Nick) Zhao.

This file provides an example for the user to use the SMT solver created in this project in solving
the graph coloring problem.
"""
import sys
sys.path.append('..')
from SMT_Solver.smt import *


def solve_graph_coloring(graph, num_colors, method='dpll'):
    if num_colors > len(list(graph.keys())):
        raise Exception("The maximum number of colors cannot be larger than the number of nodes in the graph.")

    # Formulate the SMT representation:

    # First, formulate the SMT encoding:
    smt_variables = set()
    smt_encoding = dict()
    index = 0
    for node in graph:
        connections = graph[node]
        for connected_node in connections:
            smt_encoding["x" + str(index)] = ["nq", node, connected_node]
            smt_variables.add(node)
            smt_variables.add(connected_node)
            index += 1
    smt_variables = list(smt_variables)

    if len(smt_variables) == 0:
        raise Exception("The maximum number of SMT Variables cannot be 0 for graph coloring.")

    # Now, formulate the SAT encoding:
    sat_encoding = []
    if len(smt_encoding.keys()) == 1:
        sat_encoding = list(smt_encoding.keys())[0]
    else:
        for sat_node in smt_encoding:
            if len(sat_encoding) == 0:
                sat_encoding = sat_node
            else:
                sat_encoding = ["and", sat_node, sat_encoding]

    # Find the lower and upper bound.
    lower_bound = 0
    upper_bound = num_colors - 1
    
    if method == 'robdd':
        return solve_SMT(sat_encoding, smt_encoding, smt_variables, lower_bound, upper_bound, method = "robdd")
    return solve_SMT(sat_encoding, smt_encoding, smt_variables, lower_bound, upper_bound)
