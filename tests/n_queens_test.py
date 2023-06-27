"""
Author: Yiqi (Nick) Zhao

This file tests the N-Queens Solver.

# I used the tutorial here: https://github.com/cgoldberg/python-unittest-tutorial
"""

from problems.n_queens.n_queens_solver import solve_n_queens

import unittest


def is_valid_board(board):
    """
    This helper function checks if a given board is valid for N-Queens
    (assuming the board has a correct structure).
    """
    indices = []
    # Collect the indices for the queens.
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 1:
                indices.append((i, j))

    # Ensure that no two queens are in the same row.
    row_indices = set()
    for index in indices:
        if index[0] in row_indices:
            return False
        else:
            row_indices.add(index[0])

    # Ensure that no two queens are in the same column.
    col_indices = set()
    for index in indices:
        if index[1] in col_indices:
            return False
        else:
            col_indices.add(index[1])

    # Ensure that no two queens attack each other by diagonal.
    for i in range(len(indices)):
        for j in range(len(indices)):
            if i != j:
                row_1 = indices[i][0]
                row_2 = indices[j][0]
                col_1 = indices[i][1]
                col_2 = indices[i][1]
                if abs(row_1 - row_2) == abs(col_1 - col_2):
                    return False

    # Check that the number of queens is correct.
    return len(indices) == len(board)


class NQueesTest(unittest.TestCase):

    """
    Users are encouraged to try out these tests and customize their own tests
    to gain familiarity with the software.
    """

    def test_case_UNSAT(self):
        solution = solve_n_queens(3)
        self.assertTrue(solution == "UNSAT")

    def test_case_SAT(self):
        for i in range(4, 7):
            board = solve_n_queens(i)
            self.assertTrue(is_valid_board(board))


if __name__ == '__main__':
    unittest.main()