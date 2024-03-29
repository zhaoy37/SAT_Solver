"""
Author: Yiqi (Nick) Zhao

This file tests the SMT solver.

# I used the tutorial here: https://github.com/cgoldberg/python-unittest-tutorial
"""

import sys
sys.path.insert(0, '..')
from SMT_Solver.smt import solve_SMT
import unittest

class SMTTest(unittest.TestCase):

    """
    Users are encouraged to try out these tests and customize their own tests
    to gain familiarity with the software.
    """

    def test_case_1(self):
        solution1 = solve_SMT(["and", "x1", "x2"], {"x1": ["eq", "y1 - 2", "y2"], "x2": ["gt", "y2 + y1", 5]},
                              ["y1", "y2"], 0, 10, method = "backtracking")
        y1 = solution1["y1"]
        y2 = solution1["y2"]
        self.assertTrue(y1 - 2 == y2)
        self.assertTrue(y2 + y1 > 5)

    def test_case_1r(self):
        solution1 = solve_SMT(["and", "x1", "x2"], {"x1": ["eq", "y1 - 2", "y2"], "x2": ["gt", "y2 + y1", 5]},
                              ["y1", "y2"], 0, 10, method = "robdd")
        y1 = solution1["y1"]
        y2 = solution1["y2"]
        self.assertTrue(y1 - 2 == y2)
        self.assertTrue(y2 + y1 > 5)

    def test_case_1m(self):
        solution1 = solve_SMT(["and", "x1", "x2"], {"x1": ["eq", "y1 - 2", "y2"], "x2": ["gt", "y2 + y1", 5]},
                              ["y1", "y2"], 0, 10)
        y1 = solution1["y1"]
        y2 = solution1["y2"]
        self.assertTrue(y1 - 2 == y2)
        self.assertTrue(y2 + y1 > 5)

    def test_case_2(self):
        solution2 = solve_SMT(["and", "x1", "x2"], {"x1": ["nq", "y1 - y2", "y1 + y2"], "x2": ["eq", "y2 + y1", "y1"]},
                              ["y1", "y2"], 0, 10, method = "backtracking")
        self.assertTrue(solution2 == "UNSAT")

    def test_case_2r(self):
        solution2 = solve_SMT(["and", "x1", "x2"], {"x1": ["nq", "y1 - y2", "y1 + y2"], "x2": ["eq", "y2 + y1", "y1"]},
                              ["y1", "y2"], 0, 10, method = "robdd")
        self.assertTrue(solution2 == "UNSAT")

    def test_case_2m(self):
        solution2 = solve_SMT(["and", "x1", "x2"], {"x1": ["nq", "y1 - y2", "y1 + y2"], "x2": ["eq", "y2 + y1", "y1"]},
                              ["y1", "y2"], 0, 10)
        self.assertTrue(solution2 == "UNSAT")

    def test_case_3(self):
        solution3 = solve_SMT(["and", ["and", ["not", "x1"], "x2"], "x3"],
                              {"x1": ["lt", "y1", 6], "x2": ["ge", "y1 - y2", 10], "x3": ["lt", 3, "y2"]}, ["y1", "y2"], -10, 20, method = "backtracking")
        y1 = solution3["y1"]
        y2 = solution3["y2"]
        self.assertFalse(y1 < 6)
        self.assertTrue(y1 - y2 >= 10)
        self.assertTrue(3 < y2)

    def test_case_3r(self):
        solution3 = solve_SMT(["and", ["and", ["not", "x1"], "x2"], "x3"],
                              {"x1": ["lt", "y1", 6], "x2": ["ge", "y1 - y2", 10], "x3": ["lt", 3, "y2"]}, ["y1", "y2"],
                              -10, 20, method = "robdd")
        y1 = solution3["y1"]
        y2 = solution3["y2"]
        self.assertFalse(y1 < 6)
        self.assertTrue(y1 - y2 >= 10)
        self.assertTrue(3 < y2)

    def test_case_3m(self):
        solution3 = solve_SMT(["and", ["and", ["not", "x1"], "x2"], "x3"],
                              {"x1": ["lt", "y1", 6], "x2": ["ge", "y1 - y2", 10], "x3": ["lt", 3, "y2"]}, ["y1", "y2"],
                              -10, 20)
        y1 = solution3["y1"]
        y2 = solution3["y2"]
        self.assertFalse(y1 < 6)
        self.assertTrue(y1 - y2 >= 10)
        self.assertTrue(3 < y2)

    def test_case_4(self):
        solution4 = solve_SMT(["and", "x1", "x2"], {"x1": ["nq", "y1", 10], "x2": ["eq", "y1 * y2", 100]}, ["y1", "y2"], 0, 30, method = "backtracking")
        y1 = solution4["y1"]
        y2 = solution4["y2"]
        self.assertTrue(y1 != 10)
        self.assertTrue(y1 * y2 == 100)

    def test_case_4r(self):
        solution4 = solve_SMT(["and", "x1", "x2"], {"x1": ["nq", "y1", 10], "x2": ["eq", "y1 * y2", 100]}, ["y1", "y2"],
                              0, 30, method = "robdd")
        y1 = solution4["y1"]
        y2 = solution4["y2"]
        self.assertTrue(y1 != 10)
        self.assertTrue(y1 * y2 == 100)

    def test_case_4m(self):
        solution4 = solve_SMT(["and", "x1", "x2"], {"x1": ["nq", "y1", 10], "x2": ["eq", "y1 * y2", 100]}, ["y1", "y2"],
                              0, 30)
        y1 = solution4["y1"]
        y2 = solution4["y2"]
        self.assertTrue(y1 != 10)
        self.assertTrue(y1 * y2 == 100)

    def test_case_5(self):
        solution5 = solve_SMT(["and", "x1", "x2"], {"x1": ["eq", "y1", 5], "x2": ["eq", "y2 // y1", 10]}, ["y1", "y2"],
                              -100, 100, method = "backtracking")
        y1 = solution5["y1"]
        y2 = solution5["y2"]
        self.assertTrue(y1 == 5)
        self.assertTrue(y2 // y1 == 10)

    def test_case_5r(self):
        solution5 = solve_SMT(["and", "x1", "x2"], {"x1": ["eq", "y1", 5], "x2": ["eq", "y2 // y1", 10]}, ["y1", "y2"],
                              -100, 100, method = "robdd")
        y1 = solution5["y1"]
        y2 = solution5["y2"]
        self.assertTrue(y1 == 5)
        self.assertTrue(y2 // y1 == 10)

    def test_case_5m(self):
        solution5 = solve_SMT(["and", "x1", "x2"], {"x1": ["eq", "y1", 5], "x2": ["eq", "y2 // y1", 10]}, ["y1", "y2"],
                              -100, 100)
        y1 = solution5["y1"]
        y2 = solution5["y2"]
        self.assertTrue(y1 == 5)
        self.assertTrue(y2 // y1 == 10)

    def test_case_6(self):
        solution6 = solve_SMT(["or", "x1","x2"], {"x1": ["le", "y1", 5], "x2": ["le", "y2", 3]}, ["y1", "y2"], 0, 10, method = "backtracking")
        y1 = solution6["y1"]
        y2 = solution6["y2"]
        self.assertTrue(y1 <= 5 or y2 <= 3)

    def test_case_6r(self):
        solution6 = solve_SMT(["or", "x1","x2"], {"x1": ["le", "y1", 5], "x2": ["le", "y2", 3]}, ["y1", "y2"], 0, 10, method = "robdd")
        y1 = solution6["y1"]
        y2 = solution6["y2"]
        self.assertTrue(y1 <= 5 or y2 <= 3)

    def test_case_6m(self):
        solution6 = solve_SMT(["or", "x1", "x2"], {"x1": ["le", "y1", 5], "x2": ["le", "y2", 3]}, ["y1", "y2"], 0, 10)
        y1 = solution6["y1"]
        y2 = solution6["y2"]
        self.assertTrue(y1 <= 5 or y2 <= 3)

    def test_case_7(self):
        solution7 = solve_SMT(["and", "x1", "x2"],{"x1": ["eq", "y1 + y2", "y4"], "x2": ["eq", "y4 + y3", 10]},
                              ["y1", "y2", "y3", "y4"], 0, 10, method = "backtracking")
        y1 = solution7["y1"]
        y2 = solution7["y2"]
        y3 = solution7["y3"]
        self.assertTrue(y1 + y2 + y3 == 10)

    def test_case_7r(self):
        solution7 = solve_SMT(["and", "x1", "x2"],{"x1": ["eq", "y1 + y2", "y4"], "x2": ["eq", "y4 + y3", 10]},
                              ["y1", "y2", "y3", "y4"], 0, 10, method = "robdd")
        y1 = solution7["y1"]
        y2 = solution7["y2"]
        y3 = solution7["y3"]
        self.assertTrue(y1 + y2 + y3 == 10)

    def test_case_7m(self):
        solution7 = solve_SMT(["and", "x1", "x2"], {"x1": ["eq", "y1 + y2", "y4"], "x2": ["eq", "y4 + y3", 10]},
                              ["y1", "y2", "y3", "y4"], 0, 10)
        y1 = solution7["y1"]
        y2 = solution7["y2"]
        y3 = solution7["y3"]
        self.assertTrue(y1 + y2 + y3 == 10)

    def test_case_8(self):
        solution8 = solve_SMT("x1", {"x1": ["lt", "y1", "-5"]}, ["y1"], -10, 10, method = "backtracking")
        y1 = solution8["y1"]
        self.assertTrue(y1 < -5)

    def test_case_8r(self):
        solution8 = solve_SMT("x1", {"x1": ["lt", "y1", "-5"]}, ["y1"], -10, 10, method = "robdd")
        y1 = solution8["y1"]
        self.assertTrue(y1 < -5)

    def test_case_8m(self):
        solution8 = solve_SMT("x1", {"x1": ["lt", "y1", "-5"]}, ["y1"], -10, 10, method = "minconflicts")
        y1 = solution8["y1"]
        self.assertTrue(y1 < -5)

    def test_exception(self):
        self.assertRaises(Exception, solve_SMT, ["and", "x1", "x2"],
                          {"x1": ["eq", "y1", 3], "x2": ["eq", "x3", 10]}, ["y1", "x3"], 0, 10)

    def test_exception_r(self):
        self.assertRaises(Exception, solve_SMT, ["and", "x1", "x2"],
                          {"x1": ["eq", "y1", 3], "x2": ["eq", "x3", 10]}, ["y1", "x3"], 0, 10, "robdd")

    def test_exception_m(self):
        self.assertRaises(Exception, solve_SMT, ["and", "x1", "x2"],
                          {"x1": ["eq", "y1", 3], "x2": ["eq", "x3", 10]}, ["y1", "x3"], 0, 10)


if __name__ == '__main__':
    unittest.main()