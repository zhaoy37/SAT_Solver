"""
Author: Yiqi (Nick) Zhao.

This file provides an example for the user to use the SMT solver created in this project in solving
the Subset Sum Problem.
"""

from SMT_Solver.smt import solve_SMT

def solve_subset_sum(target_list, target_sum):
    if len(target_list == 0):
        return "UNSAT"

    # Formulate the SMT encoding.
    smt_variables = set("y0")
    smt_encoding = dict()

    # I will complete this later. (let y0 - yn each in {0, 1} and set sum of yi * target_list[i] to target_sum.

    # smt_variables = list(smt_variables)