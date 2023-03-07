"""
Authors: Yiqi  (Nick) Zhao, Ziyan An
"""

# Import necessary modules.
from logic_parser import parse_logic

# Positive Example:
print(parse_logic("not (x1 and x2) and x3"))

# Another Positive Example:
print(parse_logic("x1 or (not (x1 and x2) and x3)"))

# Lexical Error Example:
# print(parse_logic("not a1 and x2 and x3"))

# Syntactic Error Example:
print(parse_logic("not x1 and ( and x3"))
