"""
Author: Yiqi (Nick) Zhao.

This file provides an example for the user to use the SMT solver created in this project in solving
the N-Queens problem.
"""
import sys
sys.path.append('..')
import numpy as np
from SMT_Solver.smt import *

def solve_n_queens(num_queens, method='dpll'):
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
    if method == 'robdd':
        solution = solve_SMT(sat_encoding, smt_encoding, smt_vars, lower_bound, upper_bound, method = "robdd")
    else:
        solution = solve_SMT(sat_encoding, smt_encoding, smt_vars, lower_bound, upper_bound)

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



