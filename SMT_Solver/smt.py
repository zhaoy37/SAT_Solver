"""
Author: Yiqi (Nick) Zhao, Ziyan An (for the robdd part)

This program solves SMT (integer signature) using a build DPLL SAT Solver.
"""

from dpll.logic_tree import Logic
from dpll.solver import solve
from bdd.robdd_solver import solve as robdd_solve
import random


def realize(variable, assignment):
    if isinstance(variable, int):
        return variable
    elif isinstance(variable, str):
        if variable[0] == 'x':
            raise Exception("SMT variables cannot start with x.")

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


def find_num_conflicts(converted, assignment):
    # Calculate the total number of conflicts instead of the conflicts caused
    # by the variable of interest (The argmin should be equivalent).
    num_conflicts = 0
    for formula in converted:
        conflict_flag = False
        # Realize the variables.
        try:
            var1 = realize(formula[1], assignment)
            var2 = realize(formula[2], assignment)
        except ZeroDivisionError:
            num_conflicts += 1
            continue
        operator = formula[0]

        # Perform checking.
        if operator == "lt":
            if var1 >= var2:
                conflict_flag =  True
        elif operator == "gt":
            if var1 <= var2:
                conflict_flag =  True
        elif operator == "ge":
            if var1 < var2:
                conflict_flag =  True
        elif operator == "le":
            if var1 > var2:
                conflict_flag =  True
        elif operator == "eq":
            if var1 != var2:
                conflict_flag =  True
        else:
            if var1 == var2:
                conflict_flag =  True
        num_conflicts += conflict_flag
    return num_conflicts

def find_conflicted_variables(converted, assignment):
    conflicted = set()

    # This function is used for the min-conflicts kernel and find the variables in conflicts.
    for formula in converted:
        conflict_flag = False
        try:
            var1 = realize(formula[1], assignment)
            var2 = realize(formula[2], assignment)
        except ZeroDivisionError:
            vars_of_interest = []
            if type(formula[1]) == str:
                vars_of_interest.extend(formula[1].split())
            if type(formula[2]) == str:
                vars_of_interest.extend(formula[2].split())

            for var in vars_of_interest:
                if (var not in ["+", "-", "*", "/", "//"]) and (not var.isnumeric()):
                    conflicted.add(var)
            continue

        operator = formula[0]

        # Perform checking.
        if operator == "lt":
            if var1 >= var2:
                conflict_flag = True
        elif operator == "gt":
            if var1 <= var2:
                conflict_flag = True
        elif operator == "ge":
            if var1 < var2:
                conflict_flag = True
        elif operator == "le":
            if var1 > var2:
                conflict_flag = True
        elif operator == "eq":
            if var1 != var2:
                conflict_flag = True
        else:
            if var1 == var2:
                conflict_flag = True

        # Adding in the variables if necessary.
        if conflict_flag:
            vars_of_interest = []
            if type(formula[1]) == str:
                vars_of_interest.extend(formula[1].split())
            if type(formula[2]) == str:
                vars_of_interest.extend(formula[2].split())

            for var in vars_of_interest:
                if (var not in ["+", "-", "*", "/", "//"]) and (not var.isnumeric()):
                    conflicted.add(var)

    return conflicted


def evaluate_assignment(converted, assignment):
    for formula in converted:
        # Realize the variables.
        try:
            var1 = realize(formula[1], assignment)
            var2 = realize(formula[2], assignment)
        except ZeroDivisionError:
            return False

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


"""
Kernels start here.
"""

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


# This is the kernel for solving SMT using min-conflicts from Constraint Satisfaction Problem.
# This algorithm can result in UNSAT even there exists a solution if the argument max_steps is too small.
def solve_SMT_minconflicts_kernel(converted, smt_vars, lowerbound, upperbound, max_steps = 99999):
    # Initially, randomly assign values to smt_vars.
    cur_assignment = dict()
    for var in smt_vars:
        cur_assignment[var] = random.randint(lowerbound, upperbound)

    for i in range(max_steps):
        if evaluate_assignment(converted, cur_assignment):
            return True, cur_assignment
        # Find all conflicted variables.
        conflicted_vars = list(find_conflicted_variables(converted, cur_assignment))
        if len(conflicted_vars) == 0:
            # There is no conflicted variable but the assignment evaluates to False.
            return False, {}
        # Randomly choose one conflicted variable.
        rand_index = random.randint(0, len(conflicted_vars) - 1)
        conflicted_var = conflicted_vars[rand_index]
        # Search for the value that minimizes the number of conflicts.
        conflicts_values= dict()
        best_num_conflicts = float("inf")
        for value in range(lowerbound, upperbound + 1):
            temp_assignment = cur_assignment.copy()
            temp_assignment[conflicted_var] = value
            num_conflicts = find_num_conflicts(converted, temp_assignment)
            if num_conflicts < best_num_conflicts:
                best_num_conflicts = num_conflicts

            if num_conflicts not in conflicts_values:
                conflicts_values[num_conflicts] = [value]
            else:
                conflicts_values[num_conflicts].append(value)

        # Break any tie randomly.
        possible_values = conflicts_values[best_num_conflicts]
        rand_index = random.randint(0, len(possible_values) - 1)
        best_value = possible_values[rand_index]
        cur_assignment[conflicted_var] = best_value

    return False, {}


"""
The main solver starts here.
"""
# Currently, the SMT solver only supports single solution
# (because I only need 1 for the NP-complete problem to be solved).
# The users are encouraged to extend the SMT solver to allow multiple solutions.
def solve_SMT(sat_formula, encodings, smt_vars, lowerbound, upperbound, method = "minconflicts"):
    """
    The list of all possible methods include:

    1. backtracking: The naive backtracking approach with a DPLL SAT Solver.
    2. robdd: The naive backtracking approach with an ROBDD SAT Solver.
    3. minconflicts (default): The min-conflicts solver for constraint satisfaction problem.
    """
    # First, solve the sat_formula.
    tree = Logic(sat_formula)

    if method == "robdd":
        sat_solutions = robdd_solve(sat_formula)
    else:
        sat_solutions = solve(tree, multiple = True)

    if sat_solutions == "UNSAT":
        return "UNSAT"

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

        # Perform recursive descent (or other algorithms)
        cur_assignment = []
        if method == "backtracking" or method == "robdd":
            success, solution = solve_SMT_kernel(converted, smt_vars, lowerbound, upperbound, cur_assignment)
        else:
            success, solution = solve_SMT_minconflicts_kernel(converted, smt_vars, lowerbound, upperbound)
        if success:
            return solution

    return "UNSAT"


if __name__ == "__main__":
    # y1 - 2 = y2, y2 + y1 > 5
    solution1 = solve_SMT(["and", "x1", "x2"], {"x1": ["eq", "y1 - 2", "y2"], "x2": ["gt", "y2 + y1", 5]},
                          ["y1", "y2"], 0, 10, method="minconflicts")
    print("Solution:", solution1)

