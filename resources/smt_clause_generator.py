"""
Author: Yiqi (Nick) Zhao

This file allows random generations of SMT clauses.
"""

from resources.logic_generator import *
import random
from SMT_Solver.smt import solve_SMT

def generate_random_sat_formula_for_SMT_clause(num_variables, depth):
    logic = generate_one_logic(num_variables, depth, False)
    tree = Logic(logic)
    while len(tree.leaves) != num_variables:
        logic = generate_one_logic(num_variables, depth, False)
        tree = Logic(logic)
    return logic

def generate_a_random_SMT_clause(num_sat_variables, num_smt_variables, depth_sat, lower_bound, upper_bound):
    # Generate a random SAT encoding.
    sat_encoding = generate_random_sat_formula_for_SMT_clause(num_sat_variables, depth_sat)
    sat_atoms = Logic(sat_encoding).leaves

    # Check if the maximum number of smt_variables is nonzero.
    if num_smt_variables <= 0:
        raise Exception("The number of SMT Variables cannot be less than or equal to 0.")

    smt_variables = set()
    smt_encoding = dict()
    while len(smt_variables) != num_smt_variables:
        # Generate random SMT encodings for the generated SAT encoding.
        smt_encoding = dict()
        comparators = ["le", "ge", "gt", "lt", "nq", "eq"]
        operators = ["+", "-", "*", "//"]
        smt_variables = set()
        for sat_atom in sat_atoms:
            # First, randomly determine the comparator.
            selected_comparator = comparators[random.randint(0, len(comparators) - 1)]
            selected_components = [selected_comparator]
            for i in range(2):
                # Randomly determine if the current component should be an integer or a string.
                if random.random() >= 0.5:
                    # Integer:
                    selected_components.append(random.randint(lower_bound, upper_bound))
                else:
                    # String:
                    # Determine the cardinality of the string.
                    if random.random() >= 0.5:
                        # The cardinality is 1.
                        if random.random() >= 0.5:
                            selected_y = "y" + str(random.randint(0, num_smt_variables - 1))
                            selected_components.append(selected_y)
                            smt_variables.add(selected_y)
                        else:
                            selected_components.append(str(random.randint(lower_bound, upper_bound)))
                    else:
                        # The cardinality is 3.
                        temp = []
                        for j in range(2):
                            if random.random() >= 0.5:
                                selected_y = "y" + str(random.randint(0, num_smt_variables - 1))
                                temp.append(selected_y)
                                smt_variables.add(selected_y)
                            else:
                                temp.append(str(random.randint(lower_bound, upper_bound)))
                        # Select an operator.
                        temp.append(operators[random.randint(0, len(operators) - 1)])
                        selected_components.append(str(temp[0]) + " " + temp[2] + " " + str(temp[1]))
                smt_encoding[sat_atom] = selected_components

    return [sat_encoding, smt_encoding, list(smt_variables), lower_bound, upper_bound]

def generate_random_SMT_clauses(num_clauses, num_sat_variables, num_smt_variables, depth_sat, lower_bound, upper_bound):
    smt_clauses = []
    for i in range(num_clauses):
        smt_clauses.append(generate_a_random_SMT_clause(num_sat_variables, num_smt_variables, depth_sat, lower_bound, upper_bound))
    return smt_clauses

if __name__ == "__main__":
    sat_encoding, smt_encoding, smt_variables, lower_bound, upper_bound = generate_a_random_SMT_clause(2, 2, 2, -10, 10)
    print(sat_encoding, smt_encoding, smt_variables, lower_bound, upper_bound)
