"""
Author: Yiqi (Nick) Zhao

This program solves SMT (integer signature) using a build DPLL SAT Solver.
"""

from dpll.logic_tree import Logic
from dpll.solver import solve


def realize(variable, assignment):
    if isinstance(variable, int):
        return variable

    variable_list = variable.split()
    if len(variable_list) == 1:
        if variable.isnumeric():
            return int(variable)
        else:
            return assignment[variable]
    else:
        # Allow +, -, *, //
        operator = variable_list[1]

        if variable_list[0].isnumeric():
            var1 = int(variable_list[0])
        else:
            var1 = assignment[variable_list[0]]

        if variable_list[2].isnumeric():
            var2 = int(variable_list[2])
        else:
            var2 = assignment[variable_list[2]]

        if operator == "+":
            return (var1 + var2)
        elif operator == "-":
            return (var1 - var2)
        elif operator == "*":
            return (var1 * var2)
        else:
            return (var1 // var2)


def evaluate_assignment(converted, assignment):
    for formula in converted:
        # Realize the variables.
        var1 = realize(formula[1], assignment)
        var2 = realize(formula[2], assignment)
        operator = formula[0]
        # Perform checking.
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
    if len(smt_vars) == len(cur_assignment):
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
# Currently, the SMT solver only supports single solution
# (because I only need 1 for the NP-complete problem to be solved).
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
                elif encoding[0] == "ge":
                    encoding[0] = "lt"
                elif encoding[0] == "gt":
                    encoding[0] = "le"
                elif encoding[0] == "lt":
                    encoding[0] = "ge"
                elif encoding[0] == "nq":
                    encoding[0] = "eq"
                else:
                    encoding[0] = "nq"
                converted.append(encoding)

        # Perform recursive descent.
        cur_assignment = []
        success, solution = solve_SMT_kernel(converted, smt_vars, lowerbound, upperbound, cur_assignment)
        if success:
            return solution

    return "UNSAT"