"""
Author: Yiqi (Nick) Zhao
This is the core solver of DPLL.
"""
import numpy as np

# construct the assignment to aid a binary assignment kernel.
def construct_assignment(num, leaves_set):
    bin_rep = np.binary_repr(num, len(leaves_set))
    assignment = dict()
    index = 0
    for leaf in leaves_set:
        assignment[leaf] = int(bin_rep[index])
        index += 1
    return assignment


# construct the recursive backtracking kernel.
def solve_kernel(tree, cur_assignment, variable_list, tree_heuristics_enabled, assignment_heuristic_enabled, solutions, multiple):
    if len(cur_assignment) == len(variable_list):
        var_dictionary = dict()
        index = 0
        for variable in variable_list:
            var_dictionary[variable] = cur_assignment[index]
            index += 1
        answer = tree.evaluate(var_dictionary, tree_heuristics_enabled)
        if answer:
            solutions.append(var_dictionary)
            # Terminate early if only one solution is needed.
            if not multiple:
                # This is a flag for early termination.
                return True
    else:
        # Try path 0.
        temp_assignment = cur_assignment.copy()
        temp_assignment.append(0)
        termination = solve_kernel(tree, temp_assignment, variable_list, tree_heuristics_enabled, assignment_heuristic_enabled, solutions, multiple)
        # Terminate early if only one solution is needed.
        if termination:
            return True
        # Try path 1.
        temp_assignment = cur_assignment.copy()
        temp_assignment.append(1)
        termination = solve_kernel(tree, temp_assignment, variable_list, tree_heuristics_enabled, assignment_heuristic_enabled, solutions, multiple)
        # Terminate early if only one solution is needed.
        if termination:
            return True


# Solution.
def solve(tree, tree_heuristic_enabled = True, assignment_heuristic_enabled = True, multiple = False):
    # Call the recursive backtracking kernel.
    variable_list = list(tree.leaves)
    cur_assignment = []
    solutions = []
    solve_kernel(tree, cur_assignment, variable_list, tree_heuristic_enabled, assignment_heuristic_enabled, solutions, multiple)

    # Detect pure literals if assignment_heuristic_enabled: To be implemented later
    if len(solutions) == 0:
            return "UNSAT"
    else:
        if multiple:
            return solutions
        else:
            return solutions[0]