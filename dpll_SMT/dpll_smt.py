"""
Author: Yiqi (Nick) Zhao

This program solves SMT (integer signature) using a build DPLL SAT Solver.
"""

from dpll.logic_tree import Logic
from dpll.solver import solve

def evaluate_assignment(converted, assignment):
    for formula in converted:
        var1 = formula[1]
        if formula[1] in assignment:
            var1 = assignment[formula[1]]
        var2 = formula[2]
        if formula[2] in assignment:
            var2 = assignment[formula[2]]

        operator = formula[0]
        if operator == "lt":
            if var1 >= var2:
                return False
        elif operator == "gt":
            if var1 <= var2:
                return False
        elif operator == "ge":
            if var1 < var2:
                return False
        elif operator == "le":
            if var1 > var2:
                return False
        elif operator == "eq":
            if var1 != var2:
                return False
        else:
            if var1 == var2:
                return False
    return True

# This is the kernel to the SMT solver.
def solve_SMT_kernel(converted, smt_vars, lowerbound, upperbound, cur_assignment):
    if len(converted) == len(cur_assignment):
        choice_assignment = dict()
        for i in range(len(smt_vars)):
            choice_assignment[smt_vars[i]] = cur_assignment[i]
        return evaluate_assignment(converted, choice_assignment), choice_assignment
    else:
        for choice in range(lowerbound, upperbound + 1):
            temp_assignment = cur_assignment.copy()
            temp_assignment.append(choice)
            success, solution = solve_SMT_kernel(converted, smt_vars, lowerbound, upperbound, temp_assignment)
            if success:
                return success, solution
        return False, {}


# This is just recursive backtracking for constraint satisfaction problem without DPLL(T).
# Currently, the SMT solver only supports single solution (because I only need 1 for the NP-complete problem to be solved).
# The users are encouraged to extend the SMT solver to allow multiple solutions.
def solve_SMT(sat_formula, encodings, smt_vars, lowerbound, upperbound):
    # First, solve the sat_formula.
    tree = Logic(sat_formula)
    sat_solutions = solve(tree, multiple = True)

    for sat_solution in sat_solutions:
        # Convert all negative clauses to positive ones.
        converted = []
        for sat_formula in encodings:
            encoding = encodings[sat_formula]
            if sat_solution[sat_formula]:
                converted.append(encoding)
            else:
                if encoding[0] == "le":
                    encoding[0] = "gt"
                    converted.append(encoding)
                elif encoding[0] == "ge":
                    encoding[0] = "lt"
                    converted.append(encoding)
                else:
                    encoding[0] = "nq"
                    converted.append(encoding)

        # Perform recursive descent.
        cur_assignment = []
        success, solution = solve_SMT_kernel(converted, smt_vars, lowerbound, upperbound, cur_assignment)
        if success:
            return solution
        else:
            return "UNSAT"

# Example:
# print(solve_SMT(["and", "x1", "x2"], {"x1": ["le", "y1", 2], "x2": ["eq", "y2", 3]}, ["y1", "y2"], 0, 10))