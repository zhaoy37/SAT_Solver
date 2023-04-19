"""
Author: Yiqi (Nick) Zhao.

This file provides an example for the user to use the SMT solver created in this project in solving
the independent set problem.
"""

from SMT_Solver.smt import solve_SMT

def solve_independent_set(graph, target_cardinality):
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


    # Assert that the sum is equal to target_cardinality.
    smt_variables = list(smt_variables)

    # Set the bounds.
    for node in smt_variables:
        smt_encoding["x" + str(index)] = ["le", node, 1]
        index += 1
        smt_encoding["x" + str(index)] = ["ge", node, 0]
        index += 1

    cur_y = smt_variables[0]
    cur_y_index = len(smt_variables)
    for i in range(len(smt_variables)):
        while("y" + str(cur_y_index) in smt_variables):
            cur_y_index += 1
        temp_y = "y" + str(cur_y_index)
        if i > 0:
            smt_encoding["x" + str(index)] = ["eq", cur_y + " + " + smt_variables[i], temp_y]
            cur_y = temp_y
            smt_variables.append(cur_y)
        index += 1
    smt_encoding["x" + str(index)] = ["eq", cur_y, target_cardinality]

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


graph = {
        "y1" : ["y2", "y3", "y4"],
        "y2": ["y3"],
        "y3": [],
        "y4": []
    }

print(solve_independent_set(graph, 2))