"""
Authors: Yiqi  (Nick) Zhao, Ziyan An
"""

# Import necessary modules.
from dpll.logic_tree import Logic
from shared.logic_parser import parse_logic

logic = Logic(parse_logic("(x1 or x2) and (not x1 or x3)"))
print(logic.evaluate({"x1" : 1, "x2" : 0, "x3" : 1}))

