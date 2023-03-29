"""
Author: Yiqi (Nick) Zhao

This program solves SMT (integer signature) using a build DPLL SAT Solver.
"""

from dpll.logic_tree import Logic
from dpll.solver import solve
import numpy as np


def solve_single_sat_iter(singlevar_encodings, doublevar_encodings, encodings, search_space, sat_solution):
    # Now, perform search space tuning on the smt atoms with two variables.
    original_searchspace = search_space.copy()
    start = True
    smaller = False
    while start or original_searchspace != search_space:
        start = False
        original_searchspace = search_space.copy()
        for sat_atom in singlevar_encodings:
            smt_atom = encodings[sat_atom]
            operator = smt_atom[0]
            var = smt_atom[1]
            invar = smt_atom[2]

            # Case of true.
            if sat_solution[sat_atom]:
                if operator == "le":
                    if search_space[var][0] > invar:
                        return "UNSAT"
                    else:
                        search_space[var] = search_space[var][:search_space[var].index(invar) + 1]
                elif operator == "ge":
                    if search_space[var][-1] < invar:
                        return "UNSAT"
                    else:
                        search_space[var] = search_space[var][search_space[var].index(invar):]
                else:
                    # Equivalence clause in this case.
                    if search_space[var][0] > invar or search_space[var][-1] < invar:
                        return "UNSAT"
                    else:
                        search_space[var] = [invar]
            # case of false.
            else:
                if operator == "le":
                    if search_space[var][-1] <= invar:
                        return "UNSAT"
                    else:
                        search_space[var] = search_space[var][search_space[var].index(max(min(search_space[var]), invar + 1)):]
                elif operator == "ge":
                    if search_space[var][0] >= invar:
                        return "UNSAT"
                    else:
                        search_space[var] = search_space[var][:search_space[var].index(min(max(search_space[var]), invar - 1)) + 1]
                else:
                    if search_space[var][0] == invar and search_space[var][-1] == invar:
                        return "UNSAT"
                    else:
                        search_space[var] = search_space[var][search_space[var].index(invar + 1):].extend(
                            search_space[var][:search_space[var].index(invar - 1) + 1])

        print(search_space)
        for sat_atom in doublevar_encodings:
            smt_atom = encodings[sat_atom]
            operator = smt_atom[0]
            var1 = smt_atom[1]
            var2 = smt_atom[2]
            range_1 = search_space[var1]
            range_2 = search_space[var2]

            # Set the flag of which variable to take.
            smaller = False
            larger = False
            if sat_solution[sat_atom]:
                if operator == "le":
                    larger = True
                    if range_1[0] > range_2[-1]:
                        return "UNSAT"
                    else:
                        search_space[var1] = search_space[var1][
                                             :search_space[var1].index(min(range_2[-1], range_1[-1])) + 1]
                elif operator == "ge":
                    smaller = True
                    if range_1[-1] < range_2[0]:
                        return "UNSAT"
                    else:
                        search_space[var1] = search_space[var1][search_space[var1].index(max(range_2[0], range_1[0])):]
                else:
                    # Equivalence clause.
                    if range_1[0] > range_2[-1] or range_1[-1] < range_2[0]:
                        return "UNSAT"
                    else:
                        search_space[var1] = search_space[var1][
                                             search_space[var1].index(max(range_2[0], range_1[0])): search_space[
                                                                                                        var1].index(
                                                 min(range_2[-1], range_1[-1])) + 1]
            else:
                if operator == "le":
                    smaller = True
                    if range_1[-1] <= range_2[0]:
                        return "UNSAT"
                    else:
                        search_space[var1] = search_space[var1][search_space[var1].index(max(range_1[0], range_2[0] + 1)):]
                elif operator == "ge":
                    larger = True
                    if range_1[0] >= range_2[-1]:
                        return "UNSAT"
                    else:
                        search_space[var1] = search_space[var1][
                                             :search_space[var1].index(min(range_2[-1] - 1, range_1[-1])) + 1]
                else:
                    if range_1[-1] <= range_2[0] and range_1[0] >= range_2[-1]:
                        return "UNSAT"
                    else:
                        search_space[var1] = list(sorted(np.setdiff1d(search_space[var1], search_space[var2])))
    return search_space, smaller


# The input logic relies on the SAT formula. However, it needs encode the
# atoms as inequality and equality clauses.

# This solver currently does not support multiple solutions (but users can modify this into
# a multiple solution solver if interested).

# The allowed operators are ("eq", "le", and "ge")
# If one encoding is single_var, the invar must be at index 2, and var must be in index 1.

def solve_SMT(sat_formula, encodings, smt_vars, lowerbound, upperbound, multiple = False):
    # First, solve the sat_formula.
    tree = Logic(sat_formula)
    sat_solutions = solve(tree, multiple = True)

    for sat_solution in sat_solutions:
        search_space = dict()
        # Fully represent the search space.
        for var in smt_vars:
            search_space[var] = [i for i in range(lowerbound, upperbound + 1)]

        # Separate single variable encodings from double variable encodings.
        singlevar_encodings = dict()
        doublevar_encodings = dict()
        for sat_atom in encodings:
            if isinstance(encodings[sat_atom][1], str) and isinstance(encodings[sat_atom][2], str):
                doublevar_encodings[sat_atom] = encodings[sat_atom]
            else:
                singlevar_encodings[sat_atom] = encodings[sat_atom]

        # Now, perform search space pruning on the smt atoms that have single variables.
        iter_solution = solve_single_sat_iter(singlevar_encodings, doublevar_encodings, encodings, search_space, sat_solution)
        if not isinstance(iter_solution, str):
            cur_space, smaller = iter_solution
            solution = dict()
            if smaller:
                for var in cur_space:
                    solution[var] = cur_space[var][0]
            else:
                for var in cur_space:
                    solution[var] = cur_space[var][-1]
            return solution

    return "UNSAT"

# some examples:
# (not (y1 <= y2)) and (y2 <= 3))
#print(solve_SMT(["and", ["not", "x1"], "x2"], {"x1" : ["le", "y1", "y2"], "x2" : ["le", "y2", 3]}, ["y1", "y2"], 0, 10))

# ((y1 = y2) and (y2 = y3) and (y3 = y4))
#print(solve_SMT(["and", ["and", "x1", "x2"], "x3"], {"x1" : ["eq", "y1", "y2"], "x2": ["eq", "y2", "y3"], "x3": ["eq", "y3", "y4"]}, ["y1", "y2", "y3", "y4"], 0, 10))

# ((y1 = y2) and (y2 = y3) and (y3 <= 5))
#print(solve_SMT(["and", ["and", "x1", "x2"], "x3"], {"x1" : ["eq", "y1", "y2"], "x2": ["eq", "y2", "y3"], "x3": ["le", "y3", 5]}, ["y1", "y2", "y3"], 0, 10))

# Some more examples.

#print(solve_SMT(["and", ["and", ["not", "x2"], ["not", "x1"]], "x3"], {"x1" : ["ge", "y1", "y2"], "x2": ["le", "y2", "y3"], "x3" : ["eq", "y3", 1]}, ["y1", "y2", "y3"], 0, 10))

#print(solve_SMT(["and", ["not", "x1"], ["not", "x2"]], {"x1" : ["le", "y1", 2], "x2": ["ge", "y1", 4]}, ["y1"], 0, 10))

print(solve_SMT(["and", ["not", "x1"], ["not", "x2"]], {"x1": ["eq", "y1", "y2"], "x2": ["eq", "y2", "y3"]}, ["y1", "y2", "y3"], 1, 4))