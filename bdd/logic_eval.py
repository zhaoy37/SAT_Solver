"""
Authors: Ziyan An
Reference: https://pythonnumericalmethods.berkeley.edu/notebooks/chapter01.05-Logial-Expressions-and-Operators.html 
           https://realpython.com/python-conditional-statements/ 

Implementations for logic evaluation. 
"""

def AND(x, y):
    if x == 1 and y == 1: 
        return 1
    else: 
        return 0

def OR(x, y):
    if x == 1 or y ==1: 
        return 1
    else: 
        return 0

def NOT(x):
    return not x

def ITE(i, t, e):
    """
    If-then-else evaluation.
    """
    return OR(AND(i, t), AND(NOT(i), e))

def eval(logic, value):
    """
    Recursively evaluate a logic expression. 
    """
    if isinstance(logic, str):
        return dict(value)[int(logic[1:])]

    if logic[0] == "and":       ## evaluates 'and' 
        left_val = eval(logic[1], value)
        right_val = eval(logic[2], value)
        return AND(left_val, right_val)
    
    elif logic[0] == "or":      ## evaluates 'or'
        left_val = eval(logic[1], value)
        right_val = eval(logic[2], value)
        return OR(left_val, right_val)
    
    elif logic[0] == "not":     ## evaluates 'not'
        left_val = eval(logic[1], value)
        return NOT(left_val)
    
    else:
        raise ValueError("Unrecognized formula type: " + logic[0])