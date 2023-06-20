"""
Author: Yiqi (Nick) Zhao

This file allows random generations of SMT clauses.
"""

from resources.logic_generator import *

def generate_random_sat_formula_for_SMT_clause(num_variables, depth):
    logic = generate_one_logic(num_variables, depth, False)
    tree = Logic(logic)
    while len(tree.leaves) != num_variables:
        logic = generate_one_logic(num_variables, depth, False)
        tree = Logic(logic)
    return logic

if __name__ == "__main__":
    print(generate_random_sat_formula_for_SMT_clause(3, 2))
