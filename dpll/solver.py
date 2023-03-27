"""
Author: Yiqi (Nick) Zhao
This is the core solver of DPLL.
"""

import numpy as np

"""
This function simplifies a formula given an assignment.
"""
def simplify(target, partial_assignment, heuristic_enabled = True):
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


def solve_kernel_with_heuristic(target, variable_list, cur_assignment, pure_positives, pure_negatives, solutions):
    if len(cur_assignment.keys()) >= len(variable_list):
        return False
    else:
        index = len(cur_assignment.keys())
        variable = variable_list[index]
        if variable in pure_positives:
            # Simplify.
            new_assignment = cur_assignment.copy()
            new_assignment[variable] = 1
            simplified = simplify(target, new_assignment)
            if simplified == "True":
                # Complete assignment.
                for i in range(index + 1, len(variable_list)):
                    new_assignment[variable_list[i]] = 1
                solutions.append(new_assignment)
                return True
            # I can further simplify here.
            else:
                if simplified == "False":
                    new_assignment = cur_assignment.copy()
                    new_assignment[variable] = 0
                    simplified = simplify(target, new_assignment)
                    if simplified == "True":
                        # Complete assignment.
                        for i in range(index + 1, len(variable_list)):
                            new_assignment[variable_list[i]] = 1
                        solutions.append(new_assignment)
                        return True
                    return solve_kernel_with_heuristic(simplified, variable_list, new_assignment,
                                                       pure_positives, pure_negatives, solutions)
                else:
                    if solve_kernel_with_heuristic(simplified, variable_list, new_assignment, pure_positives,
                                                   pure_negatives, solutions):
                        return True
                    else:
                        new_assignment = cur_assignment.copy()
                        new_assignment[variable] = 0
                        simplified = simplify(target, new_assignment)
                        if simplified == "True":
                            # Complete assignment.
                            for i in range(index + 1, len(variable_list)):
                                new_assignment[variable_list[i]] = 1
                            solutions.append(new_assignment)
                            return True
                        return solve_kernel_with_heuristic(simplified, variable_list, new_assignment,
                                                           pure_positives, pure_negatives, solutions)
        else:
            # Simplify.
            new_assignment = cur_assignment.copy()
            new_assignment[variable] = 0
            simplified = simplify(target, new_assignment)
            if simplified == "True":
                # Complete assignment.
                for i in range(index + 1, len(variable_list)):
                    new_assignment[variable_list[i]] = 1
                solutions.append(new_assignment)
                return True
            # I can further simplify here.
            else:
                if simplified == "False":
                    new_assignment = cur_assignment.copy()
                    new_assignment[variable] = 1
                    simplified = simplify(target, new_assignment)
                    if simplified == "True":
                        # Complete assignment.
                        for i in range(index + 1, len(variable_list)):
                            new_assignment[variable_list[i]] = 1
                        solutions.append(new_assignment)
                        return True
                    return solve_kernel_with_heuristic(simplified, variable_list, new_assignment,
                                                       pure_positives, pure_negatives, solutions)
                else:
                    if solve_kernel_with_heuristic(simplified, variable_list, new_assignment, pure_positives, pure_negatives, solutions):
                        return True
                    else:
                        new_assignment = cur_assignment.copy()
                        new_assignment[variable] = 1
                        simplified = simplify(target, new_assignment)
                        if simplified == "True":
                            # Complete assignment.
                            for i in range(index + 1, len(variable_list)):
                                new_assignment[variable_list[i]] = 1
                            solutions.append(new_assignment)
                            return True
                        return solve_kernel_with_heuristic(simplified, variable_list, new_assignment, pure_positives, pure_negatives, solutions)


# Solution.
def solve(tree, assignment_heuristic_enabled = True, multiple = False):
    # Call the recursive backtracking kernel.
    variable_list = list(tree.leaves)
    solutions = []
    # Tree Heuristic automatically enabled in this branch.
    cur_assignment = dict()
    target = tree.formula
    # Right now, multiple only works for the naive mode. I will add multiple option for the heuristic mode later.
    if (not assignment_heuristic_enabled):
        solve_kernel_with_no_heuristic(target, variable_list, multiple, solutions)
    else:
        if multiple:
            solve_kernel_with_no_heuristic(target, variable_list, multiple, solutions)
        else:
            solve_kernel_with_heuristic(target, variable_list, cur_assignment, tree.pure_positives, tree.pure_negatives, solutions)

    # Detect pure literals if assignment_heuristic_enabled: To be implemented later
    if len(solutions) == 0:
            return "UNSAT"
    else:
        if multiple:
            return solutions
        else:
            return solutions[0]