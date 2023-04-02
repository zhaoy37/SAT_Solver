"""
Author: Yiqi (Nick) Zhao.

This file provides an example for the user to use the SMT solver created in this project in solving
the N-Queens problem.
"""

from SMT_Solver.smt import solve_SMT

def solve_n_queens(num_queens):
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
    # for i in range(len(smt_vars)):
    #     column_1 = int(smt_vars[i][1:])
    #     for j in range(i + 1, len(smt_vars)):
    #         column_2 = int(smt_vars[j][1:])

solve_n_queens(3)



