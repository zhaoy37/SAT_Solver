"""
Authors: Yiqi  (Nick) Zhao, Ziyan An
"""

# Import necessary modules.
from dpll.logic_tree import Logic
from logic_parser import parse_logic

example = parse_logic("x1 and x2 or x3 and not x4")

Logic(example).print_tree()
print(Logic(example).formula)
print(Logic(example).leaves)

