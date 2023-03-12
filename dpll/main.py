"""
Authors: Yiqi  (Nick) Zhao, Ziyan An
"""

# Import necessary modules.
from dpll.logic_tree import Logic
from shared.logic_parser import parse_logic
from shared.logic_generator import generate_logic_trees
from solver import naive_tabular_solve


tree2 = generate_logic_trees(1, 2, 3)[0]

print(tree2.formula)
solution = naive_tabular_solve(tree2)
print(solution)
print(tree2.evaluate(solution))

