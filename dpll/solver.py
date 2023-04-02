"""
Author: Yiqi (Nick) Zhao
This is the core solver of DPLL.
"""

import numpy as np


def simplify(target, partial_assignment, heuristic_enabled = True):
    """
    This function simplifies a formula given an assignment.
    """
    if not isinstance(target, list):
        if target in partial_assignment:
            if partial_assignment[target]:
                return "True"
            else:
                return "False"
        else:
            return target
    else:
        if target[0] == "or":
            left_simplified = simplify(target[1], partial_assignment)
            right_simplified = simplify(target[2], partial_assignment)
            if heuristic_enabled:
                # Perform simplification.
                # Early termination:
                if left_simplified == "True" or right_simplified == "True":
                    return "True"
                # Unit clause:
                elif left_simplified == "False":
                    return right_simplified
                elif right_simplified == "False":
                    return left_simplified
                else:
                    return ["or", left_simplified, right_simplified]
            else:
                if left_simplified == "False" and right_simplified == "False":
                    return "False"
                elif left_simplified == "False" and right_simplified == "True":
                    return "True"
                elif left_simplified == "True" and right_simplified == "False":
                    return "True"
                elif left_simplified == "True" and right_simplified == "True":
                    return "True"
                else:
                    return ["or", left_simplified, right_simplified]
        elif target[0] == "and":
            left_simplified = simplify(target[1], partial_assignment)
            right_simplified = simplify(target[2], partial_assignment)
            if heuristic_enabled:
                # Perform simplification.
                # Early termination:
                if left_simplified == "False" or right_simplified == "False":
                    return "False"
                # Unit clause:
                if left_simplified == "True":
                    return right_simplified
                elif right_simplified == "True":
                    return left_simplified
                else:
                    return ["and", left_simplified, right_simplified]
            else:
                if left_simplified == "False" and right_simplified == "False":
                    return "False"
                elif left_simplified == "False" and right_simplified == "True":
                    return "False"
                elif left_simplified == "True" and right_simplified == "False":
                    return "False"
                elif left_simplified == "True" and right_simplified == "True":
                    return "True"
                else:
                    return ["and", left_simplified, right_simplified]
        else:
            right_simplified = simplify(target[1], partial_assignment)
            if right_simplified == "False":
                return "True"
            elif right_simplified == "True":
                return "False"
            else:
                return ["not", right_simplified]


def solve_kernel_with_no_heuristic(target, variable_list, multiple, solutions):
    """
    This is the tabular method.
    """
    for i in range(2 ** len(variable_list)):
        bin_rep = np.binary_repr(i, width = len(variable_list))
        assignment = dict()
        for i in range(len(bin_rep)):
            assignment[variable_list[i]] = int(bin_rep[i])
        # Evaluate.
        simplified = simplify(target, assignment, heuristic_enabled = False)
        if simplified == "True":
            solutions.append(assignment)
            if not multiple:
                return


def further_search(index, simplified, variable_list, new_assignment, pure_positives,
                   pure_negatives, solutions, multiple):
    """
    This function is used in solve_single for further searching and serves to help clean the codes.
    """
    if simplified == "True":
        # Complete assignment.
        for i in range(index + 1, len(variable_list)):
            new_assignment[variable_list[i]] = 1
        solutions.append(new_assignment)
        return True
    elif simplified == "False":
        # The assignment must be false.
        return False
    else:
        return solve_kernel_with_heuristic(simplified, variable_list, new_assignment,
                                           pure_positives, pure_negatives, solutions, multiple)


def solve_multiple(index, variable, target, variable_list, cur_assignment, pure_positives,
                   pure_negatives, solutions, ordering, multiple):
    """
    This function handles the case with multiple solutions.
    """
    new_assignment = cur_assignment.copy()
    new_assignment[variable] = ordering[0]
    simplified = simplify(target, new_assignment)
    # In the case that the solver finds True:
    if simplified == "True":
        # Generates all possible binary assignments that occur after the partial assignment.
        bin_length = len(variable_list) - (index + 1)
        for i in range(2 ** bin_length):
            bin_rep = np.binary_repr(i, width=len(variable_list))
            temp_assignment = new_assignment.copy()
            for j in range(index + 1, len(variable_list)):
                temp_assignment[variable_list[j]] = int(bin_rep[j])
            if temp_assignment not in solutions:
                solutions.append(temp_assignment)
        solve_kernel_with_heuristic(simplified, variable_list, new_assignment, pure_positives, pure_negatives,
                                    solutions, multiple)
    elif simplified != "False":
        solve_kernel_with_heuristic(simplified, variable_list, new_assignment, pure_positives, pure_negatives,
                                    solutions, multiple)

    new_assignment[variable] = ordering[1]
    simplified = simplify(target, new_assignment)
    # In the case that the solver finds True:
    if simplified == "True":
        # Generates all possible binary assignments that occur after the partial assignment.
        bin_length = len(variable_list) - (index + 1)
        for i in range(2 ** bin_length):
            bin_rep = np.binary_repr(i, width=len(variable_list))
            temp_assignment = new_assignment.copy()
            for j in range(index + 1, len(variable_list)):
                temp_assignment[variable_list[j]] = int(bin_rep[j])
            if temp_assignment not in solutions:
                solutions.append(temp_assignment)
        solve_kernel_with_heuristic(simplified, variable_list, new_assignment, pure_positives, pure_negatives,
                                    solutions, multiple)
    elif simplified != "False":
        solve_kernel_with_heuristic(simplified, variable_list, new_assignment, pure_positives, pure_negatives,
                                    solutions, multiple)


def solve_single(index, variable, target, variable_list, cur_assignment, pure_positives, pure_negatives,
                 solutions, ordering, multiple):
    """
    This function handles the case with solving for one solution only.
    """
    # Assign ordering[0] to the variable and try to simplify.
    new_assignment = cur_assignment.copy()
    new_assignment[variable] = ordering[0]
    simplified = simplify(target, new_assignment)
    # Case True following assigning ordering[0] to the variable: Return the correct answer.
    if simplified == "True":
        # Complete assignment.
        for i in range(index + 1, len(variable_list)):
            new_assignment[variable_list[i]] = 1
        solutions.append(new_assignment)
        return True
    # Case False following assigning ordering[0] to the variable: Try switch to ordering[1] and re-evaluate.
    elif simplified == "False":
        new_assignment[variable] = ordering[1]
        simplified = simplify(target, new_assignment)
        # If the solver attains true, return the correct answer.
        return further_search(index, simplified, variable_list, new_assignment, pure_positives, pure_negatives,
                              solutions, multiple)
    else:
        # The solver is inconclusive after assigning ordering[0] to the variable. Try to further simplify the formula.
        if solve_kernel_with_heuristic(simplified, variable_list, new_assignment, pure_positives,
                                       pure_negatives, solutions, multiple):
            return True
        else:
            # In this case, the solver resolves to false/inconclusive for assigning ordering[0] to the variable.
            new_assignment[variable] = ordering[1]
            simplified = simplify(target, new_assignment)
            return further_search(index, simplified, variable_list, new_assignment, pure_positives, pure_negatives,
                                  solutions, multiple)


def solve_kernel_with_heuristic(target, variable_list, cur_assignment, pure_positives, pure_negatives,
                                solutions, multiple):
    """
    This is the kernel for the solve function.
    """
    if len(cur_assignment.keys()) >= len(variable_list):
        # Base case: Reaches the end of assignment.
        return False
    else:
        index = len(cur_assignment.keys())
        variable = variable_list[index]
        if multiple:
            if variable in pure_positives:
                return solve_multiple(index, variable, target, variable_list, cur_assignment, pure_positives,
                                      pure_negatives, solutions, [1, 0], multiple)
            else:
                return solve_multiple(index, variable, target, variable_list, cur_assignment, pure_positives,
                                      pure_negatives, solutions, [0, 1], multiple)
        else:
            # Perform the heuristic on pure literals.
            if variable in pure_positives:
                return solve_single(index, variable, target, variable_list, cur_assignment, pure_positives,
                                    pure_negatives, solutions, [1, 0], multiple)
            else:
                return solve_single(index, variable, target, variable_list, cur_assignment, pure_positives,
                                    pure_negatives, solutions, [0, 1], multiple)


# Solution.
def solve(tree, heuristic_enabled = True, multiple = False):
    """
    This is the main entry point for solving the formula using DPLL.
    """
    # Call the recursive backtracking kernel.
    variable_list = list(tree.leaves)
    solutions = []
    # Tree Heuristic automatically enabled in this branch.
    cur_assignment = dict()
    target = tree.formula
    # Right now, multiple only works for the naive mode. I will add multiple option for the heuristic mode later.
    if (not heuristic_enabled):
        solve_kernel_with_no_heuristic(target, variable_list, multiple, solutions)
    else:
        solve_kernel_with_heuristic(target, variable_list, cur_assignment, tree.pure_positives,
                                    tree.pure_negatives, solutions, multiple)

    # Detect pure literals if assignment_heuristic_enabled: To be implemented later
    if len(solutions) == 0:
            return "UNSAT"
    else:
        if multiple:
            return solutions
        else:
            return solutions[0]