"""
Author: Yiqi (Nick) Zhao.

This file provides an example for the user to use the SMT solver created in this project in solving
the Partition Problem.
"""

from SMT_Solver.smt import *

def solve_partition(target_list, lower_bound = 0, upper_bound = 10, method = 'backtracking'):

    if len(target_list) == 0:
        return "UNSAT"

    # Formulate the SMT encoding.
    smt_variables = set()
    smt_encoding = dict()

    # Dictate the range of each variable and generate the temporary variables.
    index = 0
    list_vars = dict()
    for i in range(len(target_list)):
        smt_encoding["x" + str(index)] = ["ge", f"y{i}", 0]
        index += 1
        smt_encoding["x" + str(index)] = ["le", f"y{i}", 1]
        index += 1
        smt_variables.add(f"y{i}")
        list_vars[f"y{i}"] = i

    summation = ""
    for i in range(len(target_list)):
        if i == len(target_list) - 1:
            summation += (f"y{i} * {target_list[i]}")
        else:
            summation += (f"y{i} * {target_list[i]} + ")
    smt_encoding["x" + str(index)] = ["eq", f"({summation}) * 2", sum(target_list)]
    index += 1

    # Make sure that the sum is not 0 and is not the total cardinality.
    summation = ""
    for i in range(len(target_list)):
        if i == len(target_list) - 1:
            summation += f"y{i}"
        else:
            summation += f"y{i} + "
    smt_encoding["x" + str(index)] = ["nq", summation, 0]
    index += 1
    smt_encoding["x" + str(index)] = ["nq", summation, len(target_list)]
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
    
    solution = solve_SMT(sat_encoding, smt_encoding, smt_variables, lower_bound, upper_bound, method = method)

    if solution == "UNSAT":
        return solution

    group_0 = []
    group_1 = []
    for node in solution:
        if solution[node] == 0:
            group_0.append(target_list[list_vars[node]])
        else:
            group_1.append(target_list[list_vars[node]])

    return group_0, group_1