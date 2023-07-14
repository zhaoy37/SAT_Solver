from .smt import solve_SMT
import numpy as np

def solve_graph_coloring(graph, num_colors, method='backtracking'):
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

    return solve_SMT(sat_encoding, smt_encoding, smt_variables, lower_bound, upper_bound, method = method)


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


def solve_n_queens(num_queens, method='backtracking'):
    # For the queens to not attack each other, they must be already in different columns.
    # The algorithm needs to find the row position of each queen in different columns.

    # First, formulate the smt variables, which represent the row position of each queen.
    smt_vars = []
    for i in range(num_queens):
        smt_vars.append("y" + str(i))

    # Now, find the smt encoding.
    # Ensure that no variables are in the same row:
    smt_encoding = dict()
    index = 0
    for i in range(len(smt_vars)):
        for j in range(i + 1, len(smt_vars)):
            smt_encoding["x" + str(index)] = ["nq", smt_vars[i], smt_vars[j]]
            index += 1

    # Ensure that no variables are in the same diagonal.
    for i in range(len(smt_vars)):
        column_1 = int(smt_vars[i][1:])
        for j in range(i + 1, len(smt_vars)):
            column_2 = int(smt_vars[j][1:])
            smt_encoding["x" + str(index)] = ["nq", smt_vars[i] + " - " + smt_vars[j], column_1 - column_2]
            index += 1
            smt_encoding["x" + str(index)] = ["nq", smt_vars[i] + " - " + smt_vars[j], column_2 - column_1]
            index += 1

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
    upper_bound = num_queens - 1
    solution = solve_SMT(sat_encoding, smt_encoding, smt_vars, lower_bound, upper_bound, method=method)

    if solution == "UNSAT":
        return solution

    # Now, configure the board:
    # Use numpy array for better visualization.
    board = np.array([[0] * num_queens] * num_queens)
    for column_var in solution:
        column = int(column_var[1:])
        row = solution[column_var]
        board[row][column] = 1
    return board


def solve_partition(target_list, method='backtracking'):
    if len(target_list) == 0:
        return "UNSAT"

    # Formulate the SMT encoding.
    smt_variables = set()
    smt_encoding = dict()

    # Dictate the range of each variable and generate the temporary variables.
    index = 0
    list_vars = dict()
    summation = ""
    for i in range(len(target_list)):
        smt_variables.add(f"y{i}")
        list_vars[f"y{i}"] = i
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

    solution = solve_SMT(sat_encoding, smt_encoding, smt_variables, 0, 1, method=method)

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


def solve_subset_sum(target_list, target_sum, method='backtracking'):
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

    index = 0
    list_map = dict()
    # Now, ensure that the sum of the variables is the target sum.
    summation = ""
    for i in range(len(target_list)):
        list_var = f"y{i}"
        list_map[list_var] = i
        smt_variables.add(list_var)
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
    solution = solve_SMT(sat_encoding, smt_encoding, smt_variables, 0, 1, method = method)
    if solution == "UNSAT":
        return "UNSAT"

    final_solution = dict()
    for node in solution:
        final_solution[list_map[node]] = solution[node]

    return final_solution