"""
Author: Yiqi (Nick) Zhao
This is the core solver of DPLL.
"""
import numpy as np
from dpll.logic_tree import Logic
from shared.logic_parser import parse_logic

# construct the assignment.
def construct_assignment(num, leaves_set):
    bin_rep = np.binary_repr(num, len(leaves_set))
    assignment = dict()
    index = 0
    for leaf in leaves_set:
        assignment[leaf] = int(bin_rep[index])
        index += 1
    return assignment


# Naive solution.
def naive_solve(tree, tree_heuristic_enabled = True, multiple = False):
    solutions = []
    # This binary representation search is essentially the same as recursive backtracking.
    # I will replace it with actual recursive backtracking later to allow some assignment heuristics.
    for i in range(len(tree.leaves) ** 2):
        cur_assignment = construct_assignment(i, tree.leaves)
        if tree.evaluate(cur_assignment, tree_heuristic_enabled):
            if not multiple:
                return cur_assignment
            else:
                solutions.append(cur_assignment)

    if len(solutions) == 0:
        return "UNSAT"
    else:
        return solutions