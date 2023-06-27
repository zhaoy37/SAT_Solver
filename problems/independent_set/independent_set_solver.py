"""
Author: Yiqi (Nick) Zhao.

This file provides an example for the user to use the SMT solver created in this project in solving
the independent set problem.
"""
from SMT_Solver.smt import *


def solve_independent_set(graph, target_cardinality, method='backtracking'):

    # Check target_cardinality.
    if target_cardinality < 1:
        raise Exception("Target Cardinality must be at least 1.")

    # First, formulate the SMT encoding:
    smt_variables = set()
    smt_encoding = dict()
    index = 0
    for node in graph:
        connections = graph[node]
        smt_variables.add(node)
        for connected_node in connections:
            smt_encoding["x" + str(index)] = ["lt", node + " + " + connected_node, 2]
            smt_variables.add(connected_node)
            index += 1

    graph_nodes = list(graph.keys())
    if len(graph_nodes) == 0:
        raise Exception("Number of nodes in the graph cannot be 0.")

    # Assert that the sum is equal to target_cardinality.
    summation = ""
    for i in range(len(graph_nodes)):
        if i == len(graph_nodes) - 1:
            summation += graph_nodes[i]
        else:
            summation += (graph_nodes[i] + " + ")
    smt_encoding[summation] = ["eq", summation, target_cardinality]
    smt_variables = list(smt_variables)

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

    solution = solve_SMT(sat_encoding, smt_encoding, smt_variables, 0, 1, method = method)

    if solution == "UNSAT":
        return "UNSAT"

    # Summarize the answer.
    answer = []
    for node in solution:
        if node in graph and solution[node] == 1:
            answer.append(node)
    return answer


def find_maximum_independent_set(graph, method = 'backtracking'):
    i = 1
    solution = solve_independent_set(graph, i, method = method)
    prev_solution = solution
    while solution != "UNSAT":
        i += 1
        prev_solution = solution
        solution = solve_independent_set(graph, i, method=method)

    return prev_solution