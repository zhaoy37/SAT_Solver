"""
Authors: Yiqi  (Nick) Zhao, Ziyan An
"""

# Import necessary modules.
from dpll.logic_tree import Logic
from shared.logic_parser import parse_logic
from shared.logic_generator import generate_random_logic_trees_forced_numvariables_no_repetation

logic = Logic(parse_logic("(x1 or x2) and (not x1 or x3)"))
print(logic.evaluate({"x1" : 1, "x2" : 0, "x3" : 1}))

logics = generate_random_logic_trees_forced_numvariables_no_repetation(10, 3, 2)
for logic in logics:
    print(logic.formula)

