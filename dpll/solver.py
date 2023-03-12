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



# Naive tabular solution.
def naive_tabular_solve(tree, tree_heuristic_enabled = True):
    for i in range(len(tree.leaves) ** 2):
        cur_assignment = construct_assignment(i, tree.leaves)
        if tree.evaluate(cur_assignment, tree_heuristic_enabled):
            return cur_assignment
    return "UNSAT"