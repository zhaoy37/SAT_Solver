"""
Author: Yiqi (Nick) Zhao

This file tests the SMT solver.
"""

from SMT_Solver.smt import solve_SMT

def test_solve_SMT():
    # Test Case 1:
    solution1 = solve_SMT(["and", "x1", "x2"], {"x1": ["eq", "y1 - 2", "y2"], "x2": ["gt", "y2 + y1", 5]}, ["y1", "y2"], 0, 10)
    y1 = solution1["y1"]
    y2 = solution1["y2"]
    assert(y1 - 2 == y2)
    assert(y2 + y1 > 5)

    # Test Case 2:
    solution2 = solve_SMT(["and", "x1", "x2"], {"x1": ["nq", "y1 - y2", "y1 + y2"], "x2": ["eq", "y2 + y1", "y1"]}, ["y1", "y2"], 0, 10)



if __name__ == "__main__":
    test_solve_SMT()