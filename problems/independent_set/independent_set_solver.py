"""
Author: Yiqi (Nick) Zhao.

This file provides an example for the user to use the SMT solver created in this project in solving
the independent set problem.
"""
import sys
sys.path.append('..')
from SMT_Solver.smt import solve_SMT

def solve_independent_set(graph, target_cardinality):

    # Check target_cardinality.
    if target_cardinality < 1:
        raise Exception("Target Cardinality must be at least 1.")

    # First, formulate the SMT encoding:
    smt_variables = set()
    smt_encoding = dict()
    index = 0
    for node in graph:
        connections = graph[node]
        for connected_node in connections:
            smt_encoding["x" + str(index)] = ["lt", node + " + " + connected_node, 2]
            smt_variables.add(node)
            smt_variables.add(connected_node)
            index += 1

    graph_nodes = list(graph.keys())
    if len(graph_nodes) == 0:
        raise Exception("Number of nodes in the graph cannot be 0.")

    # Set the bounds.
    for node in graph_nodes:
        smt_encoding["x" + str(index)] = ["le", node, 1]
        index += 1
        smt_encoding["x" + str(index)] = ["ge", node, 0]
        index += 1
        smt_variables.add(node)

    # Assert that the sum is equal to target_cardinality.
    cur_y = graph_nodes[0]
    cur_y_index = len(graph_nodes)
    for i in range(len(graph_nodes)):
        while("y" + str(cur_y_index) in smt_variables):
            cur_y_index += 1
        temp_y = "y" + str(cur_y_index)
        if i > 0:
            smt_encoding["x" + str(index)] = ["eq", cur_y + " + " + graph_nodes[i], temp_y]
            cur_y = temp_y
            smt_variables.add(cur_y)
            smt_variables.add(graph_nodes[i])
            smt_variables.add(temp_y)
        index += 1
    smt_encoding["x" + str(index)] = ["eq", cur_y, target_cardinality]
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
    # Find the lower and upper bound.
    lower_bound = 0
    upper_bound = target_cardinality

    solution =  solve_SMT(sat_encoding, smt_encoding, smt_variables, lower_bound, upper_bound)

    if solution == "UNSAT":
        return "UNSAT"

    # Summarize the answer.
    answer = []
    for node in solution:
        if node in graph and solution[node] == 1:
            answer.append(node)
    return answer


def find_maximum_independent_set(graph):
    i = 1
    solution = solve_independent_set(graph, i)
    prev_solution = solution
    while solution != "UNSAT":
        i += 1
        prev_solution = solution
        solution = solve_independent_set(graph, i)

    return prev_solution