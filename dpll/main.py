"""
Authors: Yiqi  (Nick) Zhao, Ziyan An
"""

# Import necessary modules.
from dpll.logic_tree import Logic
from shared.logic_parser import parse_logic
from shared.logic_generator import generate_logic_trees
from solver import naive_tabular_solve

# Time some executions following this link:
# https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-executi
import time

tree2 = generate_logic_trees(1, 2, 5)[0]

print(tree2.formula)

noheuristic = time.time()
solution = naive_tabular_solve(tree2, False)
print("---Execution with no Heuristic (naive): %s seconds --- " % (time.time() - noheuristic))
print(solution)

heuristic = time.time()
solution = naive_tabular_solve(tree2, True)
print("---Execution with heurisitc (naive): %s seconds --- " % (time.time() - heuristic))
print(solution)

print(tree2.evaluate(solution))

