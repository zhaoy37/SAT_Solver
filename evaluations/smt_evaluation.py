"""
Author: Yiqi (Nick) Zhao

This file evaluates the SMT solver with 3 case studies.
It duplicates many tests from /tests/smt_solver_test.py
"""

from SMT_Solver.smt import solve_SMT

import unittest

class SMTTest(unittest.TestCase):

    """
    Users are encouraged to try out these tests and customize their own tests
    to gain familiarity with the software.
    """

    def test_case_1(self):
        solution1 = solve_SMT(["and", "x1", "x2"], {"x1": ["eq", "y1 - 2", "y2"], "x2": ["gt", "y2 + y1", 5]},
                              ["y1", "y2"], 0, 10)
        y1 = solution1["y1"]
        y2 = solution1["y2"]
        print(f"Test case 1: y1: {y1}, y2: {y2}")
        self.assertTrue(y1 - 2 == y2)
        self.assertTrue(y2 + y1 > 5)

    def test_case_2(self):
        solution2 = solve_SMT(["and", "x1", "x2"], {"x1": ["nq", "y1 - y2", "y1 + y2"], "x2": ["eq", "y2 + y1", "y1"]},
                              ["y1", "y2"], 0, 10)
        print(f"Test case 2: {solution2}")
        self.assertTrue(solution2 == "UNSAT")

    def test_case_3(self):
        solution3 = solve_SMT(["and", ["and", ["not", "x1"], "x2"], "x3"],
                              {"x1": ["lt", "y1", 6], "x2": ["ge", "y1 - y2", 10], "x3": ["lt", 3, "y2"]}, ["y1", "y2"], -10, 20)
        y1 = solution3["y1"]
        y2 = solution3["y2"]
        print(f"Test case 3: y1 : {y1}, y2: {y2}")
        self.assertFalse(y1 < 6)
        self.assertTrue(y1 - y2 >= 10)
        self.assertTrue(3 < y2)

    def test_case_4(self):
        solution4 = solve_SMT(["and", "x1", "x2"], {"x1": ["nq", "y1", 10], "x2": ["eq", "y1 * y2", 100]}, ["y1", "y2"], 0, 30)
        y1 = solution4["y1"]
        y2 = solution4["y2"]
        print(f"Test case 4: y1: {y1}, y2:{y2}")
        self.assertTrue(y1 != 10)
        self.assertTrue(y1 * y2 == 100)

    def test_case_5(self):
        solution5 = solve_SMT(["and", "x1", "x2"], {"x1": ["eq", "y1", 5], "x2": ["eq", "y2 // y1", 10]}, ["y1", "y2"],
                              -100, 100)
        y1 = solution5["y1"]
        y2 = solution5["y2"]
        print(f"Test case 5: y1: {y1}, y2: {y2}")
        self.assertTrue(y1 == 5)
        self.assertTrue(y2 // y1 == 10)

    def test_case_6(self):
        solution6 = solve_SMT(["or", "x1","x2"], {"x1": ["le", "y1", 5], "x2": ["le", "y2", 3]}, ["y1", "y2"], 0, 10)
        y1 = solution6["y1"]
        y2 = solution6["y2"]
        print(f"Test case 6: y1: {y1}, y2: {y2}")
        self.assertTrue(y1 <= 5 or y2 <= 3)

    def test_case_7(self):
        solution7 = solve_SMT(["and", "x1", "x2"],{"x1": ["eq", "y1 + y2", "y4"], "x2": ["eq", "y4 + y3", 10]},
                              ["y1", "y2", "y3", "y4"], 0, 10)
        y1 = solution7["y1"]
        y2 = solution7["y2"]
        y3 = solution7["y3"]
        print(f"Test case 7: y1: {y1}, y2: {y2}, y3: {y3}")
        self.assertTrue(y1 + y2 + y3 == 10)

    def test_case_8(self):
        solution8 = solve_SMT(["and", "x1", ["not", "x1"]], {"x1": ["eq", "y1", "y2"]}, ["y1", "y2"], 0, 10)
        print(f"Test case 8: {solution8}")
        self.assertTrue(solution8 == "UNSAT")

    def test_case_9(self):
        solution1 = solve_SMT(["and", "x1", "x2"], {"x1": ["eq", "y1 - 2", "y2"], "x2": ["gt", "y2 + y1", 5]},
                              ["y1", "y2"], 0, 10, method = "robdd")
        y1 = solution1["y1"]
        y2 = solution1["y2"]
        print(f"Test case 1: y1: {y1}, y2: {y2}")
        self.assertTrue(y1 - 2 == y2)
        self.assertTrue(y2 + y1 > 5)

    def test_case_10(self):
        solution2 = solve_SMT(["and", "x1", "x2"], {"x1": ["nq", "y1 - y2", "y1 + y2"], "x2": ["eq", "y2 + y1", "y1"]},
                              ["y1", "y2"], 0, 10, method = "robdd")
        print(f"Test case 2: {solution2}")
        self.assertTrue(solution2 == "UNSAT")

    def test_case_11(self):
        solution3 = solve_SMT(["and", ["and", ["not", "x1"], "x2"], "x3"],
                              {"x1": ["lt", "y1", 6], "x2": ["ge", "y1 - y2", 10], "x3": ["lt", 3, "y2"]}, ["y1", "y2"], -10, 20,
                              method = "robdd")
        y1 = solution3["y1"]
        y2 = solution3["y2"]
        print(f"Test case 3: y1 : {y1}, y2: {y2}")
        self.assertFalse(y1 < 6)
        self.assertTrue(y1 - y2 >= 10)
        self.assertTrue(3 < y2)

    def test_case_12(self):
        solution4 = solve_SMT(["and", "x1", "x2"], {"x1": ["nq", "y1", 10], "x2": ["eq", "y1 * y2", 100]}, ["y1", "y2"],
                              0, 30, method = "robdd")
        y1 = solution4["y1"]
        y2 = solution4["y2"]
        print(f"Test case 4: y1: {y1}, y2:{y2}")
        self.assertTrue(y1 != 10)
        self.assertTrue(y1 * y2 == 100)

    def test_case_13(self):
        solution5 = solve_SMT(["and", "x1", "x2"], {"x1": ["eq", "y1", 5], "x2": ["eq", "y2 // y1", 10]}, ["y1", "y2"],
                              -100, 100, method = "robdd")
        y1 = solution5["y1"]
        y2 = solution5["y2"]
        print(f"Test case 5: y1: {y1}, y2: {y2}")
        self.assertTrue(y1 == 5)
        self.assertTrue(y2 // y1 == 10)

    def test_case_14(self):
        solution6 = solve_SMT(["or", "x1","x2"], {"x1": ["le", "y1", 5], "x2": ["le", "y2", 3]}, ["y1", "y2"], 0, 10,
                              method = "robdd")
        y1 = solution6["y1"]
        y2 = solution6["y2"]
        print(f"Test case 6: y1: {y1}, y2: {y2}")
        self.assertTrue(y1 <= 5 or y2 <= 3)

    def test_case_15(self):
        solution7 = solve_SMT(["and", "x1", "x2"],{"x1": ["eq", "y1 + y2", "y4"], "x2": ["eq", "y4 + y3", 10]},
                              ["y1", "y2", "y3", "y4"], 0, 10, method = "robdd")
        y1 = solution7["y1"]
        y2 = solution7["y2"]
        y3 = solution7["y3"]
        print(f"Test case 7: y1: {y1}, y2: {y2}, y3: {y3}")
        self.assertTrue(y1 + y2 + y3 == 10)

    def test_case_16(self):
        solution8 = solve_SMT(["and", "x1", ["not", "x1"]], {"x1": ["eq", "y1", "y2"]}, ["y1", "y2"], 0, 10,
                              method = "robdd")
        print(f"Test case 8: {solution8}")
        self.assertTrue(solution8 == "UNSAT")

    def test_case_17(self):
        solution1 = solve_SMT(["and", "x1", "x2"], {"x1": ["eq", "y1 - 2", "y2"], "x2": ["gt", "y2 + y1", 5]},
                              ["y1", "y2"], 0, 10, method = "backtracking")
        y1 = solution1["y1"]
        y2 = solution1["y2"]
        print(f"Test case 1: y1: {y1}, y2: {y2}")
        self.assertTrue(y1 - 2 == y2)
        self.assertTrue(y2 + y1 > 5)

    def test_case_18(self):
        solution2 = solve_SMT(["and", "x1", "x2"], {"x1": ["nq", "y1 - y2", "y1 + y2"], "x2": ["eq", "y2 + y1", "y1"]},
                              ["y1", "y2"], 0, 10, method = "backtracking")
        print(f"Test case 2: {solution2}")
        self.assertTrue(solution2 == "UNSAT")

    def test_case_19(self):
        solution3 = solve_SMT(["and", ["and", ["not", "x1"], "x2"], "x3"],
                              {"x1": ["lt", "y1", 6], "x2": ["ge", "y1 - y2", 10], "x3": ["lt", 3, "y2"]}, ["y1", "y2"],
                              -10, 20, method = "backtracking")
        y1 = solution3["y1"]
        y2 = solution3["y2"]
        print(f"Test case 3: y1 : {y1}, y2: {y2}")
        self.assertFalse(y1 < 6)
        self.assertTrue(y1 - y2 >= 10)
        self.assertTrue(3 < y2)

    def test_case_20(self):
        solution4 = solve_SMT(["and", "x1", "x2"], {"x1": ["nq", "y1", 10], "x2": ["eq", "y1 * y2", 100]}, ["y1", "y2"],
                              0, 30, method = "backtracking")
        y1 = solution4["y1"]
        y2 = solution4["y2"]
        print(f"Test case 4: y1: {y1}, y2:{y2}")
        self.assertTrue(y1 != 10)
        self.assertTrue(y1 * y2 == 100)

    def test_case_21(self):
        solution5 = solve_SMT(["and", "x1", "x2"], {"x1": ["eq", "y1", 5], "x2": ["eq", "y2 // y1", 10]}, ["y1", "y2"],
                              -100, 100, method = "backtracking")
        y1 = solution5["y1"]
        y2 = solution5["y2"]
        print(f"Test case 5: y1: {y1}, y2: {y2}")
        self.assertTrue(y1 == 5)
        self.assertTrue(y2 // y1 == 10)

    def test_case_22(self):
        solution6 = solve_SMT(["or", "x1","x2"], {"x1": ["le", "y1", 5], "x2": ["le", "y2", 3]}, ["y1", "y2"], 0, 10,
                              method = "backtracking")
        y1 = solution6["y1"]
        y2 = solution6["y2"]
        print(f"Test case 6: y1: {y1}, y2: {y2}")
        self.assertTrue(y1 <= 5 or y2 <= 3)

    def test_case_23(self):
        solution7 = solve_SMT(["and", "x1", "x2"],{"x1": ["eq", "y1 + y2", "y4"], "x2": ["eq", "y4 + y3", 10]},
                              ["y1", "y2", "y3", "y4"], 0, 10, method = "backtracking")
        y1 = solution7["y1"]
        y2 = solution7["y2"]
        y3 = solution7["y3"]
        print(f"Test case 7: y1: {y1}, y2: {y2}, y3: {y3}")
        self.assertTrue(y1 + y2 + y3 == 10)

    def test_case_24(self):
        solution8 = solve_SMT(["and", "x1", ["not", "x1"]], {"x1": ["eq", "y1", "y2"]}, ["y1", "y2"], 0, 10,
                              method = "backtracking")
        print(f"Test case 8: {solution8}")
        self.assertTrue(solution8 == "UNSAT")


if __name__ == '__main__':
    unittest.main()