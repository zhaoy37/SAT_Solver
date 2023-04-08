"""
Author: Yiqi (Nick) Zhao

This file tests the subset sum solver.

# I used the tutorial here: https://github.com/cgoldberg/python-unittest-tutorial
"""

from problems.subset_sum.subset_sum_solver import solve_subset_sum

import unittest

class SumTest(unittest.TestCase):

    """
    Users are encouraged to try out these tests and customize their own tests
    to gain familiarity with the software.
    """
    def test_case_1(self):
        solution = solve_subset_sum([2, 3], 5)
        self.assertTrue(solution[0] == 1)
        self.assertTrue(solution[1] == 1)

    def test_case_2(self):
        solution = solve_subset_sum([2, 3], 2)
        self.assertTrue(solution[0] == 1)
        self.assertTrue(solution[1] == 0)

    def test_case_3(self):
        solution = solve_subset_sum([1], 1)
        self.assertTrue(solution[0] == 1)

    def test_case_4(self):
        solution = solve_subset_sum([2, 3], 1)
        self.assertTrue(solution == "UNSAT")

    def test_case_5(self):
        solution = solve_subset_sum([], 3)
        self.assertTrue(solution == "UNSAT")

if __name__ == '__main__':
    unittest.main()