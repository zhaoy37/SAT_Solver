"""
Author: Yiqi (Nick) Zhao.

This file provides an example for the user to use the SMT solver created in this project in solving
the Subset Sum Problem.
"""

from SMT_Solver.smt import solve_SMT

def solve_subset_sum(target_list, target_sum, lower_bound = 0, upper_bound = 10):
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

    # Add product temporary variables.
    index = 0
    temp_variables = set()
    list_vars = set()
    list_map = dict()
    for i in range(len(target_list)):
        temp_var = f"y{len(target_list) + index}"
        list_var = f"y{i}"
        smt_encoding["x" + str(index)] = ["eq", f"{list_var} * {target_list[i]}", temp_var]
        index += 1
        # Bound the encoding of the list variables.
        smt_encoding["x" + str(index)] = ["ge", f"{list_var}", 0]
        index += 1
        smt_encoding["x" + str(index)] = ["le", f"{list_var}", 1]
        index += 1
        smt_variables.add(temp_var)
        smt_variables.add(list_var)
        temp_variables.add(temp_var)
        list_vars.add(list_var)
        list_map[list_var] = i

    # Now, ensure that the sum of the temporary variables is the target sum.
    cur_temp = ""
    for var in temp_variables:
        if cur_temp == "":
            cur_temp = var
        else:
            smt_encoding["x" + str(index)] = ["eq", var + " + " + cur_temp, f"y{len(target_list) + index}"]
            cur_temp = f"y{len(target_list) + index}"
            smt_variables.add(cur_temp)
            index += 1

    # Set the final sum to be equal to the target sum.
    smt_encoding["x" + str(index)] = ["eq", cur_temp, target_sum]
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

    solution = solve_SMT(sat_encoding, smt_encoding, smt_variables, lower_bound, upper_bound)
    if solution == "UNSAT":
        return "UNSAT"

    final_solution = dict()
    for node in solution:
        if node in list_vars:
            final_solution[list_map[node]] = solution[node]

    return final_solution