"""
Author: Yiqi (Nick) Zhao

This file tests the DPLL SAT Solver (and the logic tree).

# I used the tutorial here: https://github.com/cgoldberg/python-unittest-tutorial
"""

from dpll.solver import solve
from shared.logic_parser import parse_logic
from dpll.logic_tree import Logic

import unittest


def find_solution(representation, enabled = True):
    """
    This helper function helps to test the solver.
    """
    formula = parse_logic(representation)
    tree = Logic(formula)
    return solve(tree, heuristic_enabled = enabled)


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

if __name__ == '__main__':
    unittest.main()