"""
Author: Yiqi (Nick) Zhao

This file tests the DPLL SAT Solver (and the logic tree).

# I used the tutorial here: https://github.com/cgoldberg/python-unittest-tutorial
"""

from dpll.solver import solve
from resources.logic_parser import parse_logic
from dpll.logic_tree import Logic
import numpy as np

import unittest


def find_solution(representation, enabled = True, multiple_solutions = False):
    """
    This helper function helps to test the solver.
    """
    formula = parse_logic(representation)
    tree = Logic(formula)
    return solve(tree, heuristic_enabled = enabled, multiple = multiple_solutions)


class SATSolverTest(unittest.TestCase):

    """
    Users are encouraged to try out these tests and customize their own tests
    to gain familiarity with the software.
    """
    def test_heuristic_enabled_single_case_1(self):
        solution = find_solution("x1 and x2")
        x1 = solution["x1"]
        x2 = solution["x2"]
        self.assertTrue(x1 and x2)

    def test_heuristic_enabled_single_case_2(self):
        solution = find_solution("x1 and x2 or not x3 and x4 or not x5 and x1")
        x1, x2, x3, x4, x5 = solution["x1"], solution["x2"], solution["x3"], solution["x4"], solution["x5"]
        self.assertTrue(x1 and x2 or not x3 and x4 or not x5 and x1)

    def test_heuristic_enabled_single_case_3(self):
        solution = find_solution("(x1 or x2) and x3 or not x1")
        x1, x2, x3 = solution["x1"], solution["x2"], solution["x3"]
        self.assertTrue((x1 or x2) and x3 or not x1)

    def test_heuristic_enabled_single_case_4(self):
        solution = find_solution("x1 and not x1")
        self.assertTrue(solution == "UNSAT")

    def test_heuristic_disabled_single_case_1(self):
        solution = find_solution("x1 and x2", enabled = False)
        x1 = solution["x1"]
        x2 = solution["x2"]
        self.assertTrue(x1 and x2)

    def test_heuristic_disabled_single_case_2(self):
        solution = find_solution("x1 and x2 or not x3 and x4 or not x5 and x1", enabled = False)
        x1, x2, x3, x4, x5 = solution["x1"], solution["x2"], solution["x3"], solution["x4"], solution["x5"]
        self.assertTrue(x1 and x2 or not x3 and x4 or not x5 and x1)

    def test_heuristic_disabled_single_case_3(self):
        solution = find_solution("(x1 or x2) and x3 or not x1", enabled = False)
        x1, x2, x3 = solution["x1"], solution["x2"], solution["x3"]
        self.assertTrue((x1 or x2) and x3 or not x1)

    def test_heuristic_disabled_single_case_4(self):
        solution = find_solution("x1 and not x1", enabled = False)
        self.assertTrue(solution == "UNSAT")

    def test_heuristic_enabled_multiple_case_1(self):
        solutions = find_solution("x1 or x2 or x3", multiple_solutions = True)
        self.assertTrue(len(solutions) == 7)
        for solution in solutions:
            x1, x2, x3 = solution["x1"], solution["x2"], solution["x3"]
            self.assertTrue(x1 or x2 or x3)

    def test_heuristic_enabled_multiple_case_2(self):
        solutions = find_solution("x1 and x2 or not x3 and x4 or not x5 and x1", multiple_solutions=True)
        # First, find the number of possible solutions using the tabular method.
        num_solutions = 0
        for i in range(2 ** 5):
            bin = np.binary_repr(i, width = 5)
            candidate = dict()
            for i in range(1, 6):
                candidate["x" + str(i)] = int(bin[i - 1])
            x1, x2, x3, x4, x5 = candidate["x1"], candidate["x2"], candidate["x3"], candidate["x4"], candidate["x5"]
            if x1 and x2 or not x3 and x4 or not x5 and x1:
                num_solutions += 1

        self.assertTrue(num_solutions, len(solutions))
        for solution in solutions:
            x1, x2, x3, x4, x5 = solution["x1"], solution["x2"], solution["x3"], solution["x4"], solution["x5"]
            self.assertTrue(x1 and x2 or not x3 and x4 or not x5 and x1)

    def test_heuristic_enabled_multiple_case_3(self):
        solutions = find_solution("(x1 or x2) and x3 or not x1", multiple_solutions=True)
        # First, find the number of possible solutions using the tabular method.
        num_solutions = 0
        for i in range(2 ** 3):
            bin = np.binary_repr(i, width=5)
            candidate = dict()
            for i in range(1, 4):
                candidate["x" + str(i)] = int(bin[i - 1])
            x1, x2, x3 = candidate["x1"], candidate["x2"], candidate["x3"]
            if (x1 or x2) and x3 or not x1:
                num_solutions += 1

        self.assertTrue(num_solutions, len(solutions))
        for solution in solutions:
            x1, x2, x3 = solution["x1"], solution["x2"], solution["x3"]
            self.assertTrue((x1 or x2) and x3 or not x1)

    def test_heuristic_enabled_multiple_case_4(self):
        solutions = find_solution("x1 and not x1", multiple_solutions=True)
        self.assertTrue(solutions == "UNSAT")

    def test_heuristic_disabled_multiple_case_1(self):
        solutions = find_solution("x1 or x2 or x3", multiple_solutions = True, enabled = False)
        self.assertTrue(len(solutions) == 7)
        for solution in solutions:
            x1, x2, x3 = solution["x1"], solution["x2"], solution["x3"]
            self.assertTrue(x1 or x2 or x3)

    def test_heuristic_disabled_multiple_case_2(self):
        solutions = find_solution("x1 and x2 or not x3 and x4 or not x5 and x1", multiple_solutions=True, enabled = False)
        # First, find the number of possible solutions using the tabular method.
        num_solutions = 0
        for i in range(2 ** 5):
            bin = np.binary_repr(i, width = 5)
            candidate = dict()
            for i in range(1, 6):
                candidate["x" + str(i)] = int(bin[i - 1])
            x1, x2, x3, x4, x5 = candidate["x1"], candidate["x2"], candidate["x3"], candidate["x4"], candidate["x5"]
            if x1 and x2 or not x3 and x4 or not x5 and x1:
                num_solutions += 1

        self.assertTrue(num_solutions, len(solutions))
        for solution in solutions:
            x1, x2, x3, x4, x5 = solution["x1"], solution["x2"], solution["x3"], solution["x4"], solution["x5"]
            self.assertTrue(x1 and x2 or not x3 and x4 or not x5 and x1)

    def test_heuristic_disabled_multiple_case_3(self):
        solutions = find_solution("(x1 or x2) and x3 or not x1", multiple_solutions=True, enabled = False)
        # First, find the number of possible solutions using the tabular method.
        num_solutions = 0
        for i in range(2 ** 3):
            bin = np.binary_repr(i, width=5)
            candidate = dict()
            for i in range(1, 4):
                candidate["x" + str(i)] = int(bin[i - 1])
            x1, x2, x3 = candidate["x1"], candidate["x2"], candidate["x3"]
            if (x1 or x2) and x3 or not x1:
                num_solutions += 1

        self.assertTrue(num_solutions, len(solutions))
        for solution in solutions:
            x1, x2, x3 = solution["x1"], solution["x2"], solution["x3"]
            self.assertTrue((x1 or x2) and x3 or not x1)

    def test_heuristic_disabled_multiple_case_4(self):
        solutions = find_solution("x1 and not x1", multiple_solutions=True, enabled = False)
        self.assertTrue(solutions == "UNSAT")


if __name__ == '__main__':
    unittest.main()