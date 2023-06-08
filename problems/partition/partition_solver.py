"""
Author: Yiqi (Nick) Zhao.

This file provides an example for the user to use the SMT solver created in this project in solving
the Partition Problem.
"""

from SMT_Solver.smt import *

def solve_partition(target_list, lower_bound = 0, upper_bound = 10, method = 'dpll'):

    if len(target_list) == 0:
        return "UNSAT"

    # Formulate the SMT encoding.
    smt_variables = set()
    smt_encoding = dict()

    # Dictate the range of each variable and generate the temporary variables.
    index = 0
    temp_vars = set()
    list_vars = dict()
    for i in range(len(target_list)):
        list_var = f"y{i}"
        temp_var = f"y{len(target_list) + i}"
        temp_vars.add(temp_var)
        smt_encoding["x" + str(index)] = ["ge", f"{list_var}", 0]
        index += 1
        smt_encoding["x" + str(index)] = ["le", f"{list_var}", 1]
        index += 1
        smt_encoding["x" + str(index)] = ["eq", f"{list_var} * {target_list[i]}", temp_var]
        index += 1
        smt_variables.add(list_var)
        list_vars[list_var] = i
        smt_variables.add(temp_var)

    # Find the sum of the temporary variables.
    cur_temp = ""
    for var in temp_vars:
        if cur_temp == "":
            cur_temp = var
        else:
            smt_encoding["x" + str(index)] = ["eq", var + " + " + cur_temp, f"y{len(target_list) + index}"]
            cur_temp = f"y{len(target_list) + index}"
            smt_variables.add(cur_temp)
            index += 1
    group_sum = cur_temp

    # Find the total_sum.
    smt_encoding["x" + str(index)] = ["eq", f"{group_sum} * 2", sum(target_list)]
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
    
    if method == 'robdd':
        solution = solve_SMT(sat_encoding, smt_encoding, smt_variables, lower_bound, upper_bound, method = "robdd")
    else:
        solution = solve_SMT(sat_encoding, smt_encoding, smt_variables, lower_bound, upper_bound)

    if solution == "UNSAT":
        return solution

    group_0 = []
    group_1 = []
    for node in solution:
        if node in list_vars:
            if solution[node] == 0:
                group_0.append(target_list[list_vars[node]])
            else:
                group_1.append(target_list[list_vars[node]])

    return group_0, group_1