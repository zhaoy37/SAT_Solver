"""
Author: Yiqi (Nick) Zhao.

This file provides an example for the user to use the SMT solver created in this project in solving
the Subset Sum Problem.
"""

from SMT_Solver.smt import *


def solve_subset_sum(target_list, target_sum, lower_bound = 0, upper_bound = 10, method='backtracking'):
    for value in target_list:
        if value <= 0:
            raise Exception("List element must be positive.")

    if len(target_list) == 0:
        return "UNSAT"

    if not isinstance(target_sum, int):
        raise Exception("Invalid type for target_sum.")

    # Formulate the SMT encoding.
    smt_variables = set()
    smt_encoding = dict()

    # Dictate the bound on the variables.
    index = 0
    list_map = dict()
    for i in range(len(target_list)):
        list_var = f"y{i}"
        # Bound the encoding of the list variables.
        smt_encoding["x" + str(index)] = ["ge", f"{list_var}", 0]
        index += 1
        smt_encoding["x" + str(index)] = ["le", f"{list_var}", 1]
        index += 1
        smt_variables.add(list_var)
        list_map[list_var] = i

    # Now, ensure that the sum of the variables is the target sum.
    summation = ""
    for i in range(len(target_list)):
        if i == len(target_list) - 1:
            summation += f"y{i} * {target_list[i]}"
        else:
            summation += f"y{i} * {target_list[i]}+ "
    smt_encoding["x" + str(index)] = ["eq", summation, target_sum]
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
        return "UNSAT"

    final_solution = dict()
    for node in solution:
        final_solution[list_map[node]] = solution[node]

    return final_solution