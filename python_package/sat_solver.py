from .logic_parser import parse_logic
from .logic_tree import Logic
from .solver import solve as dpll_solve
from .robdd_solver import solve as robdd_solve

def sat_solve(formula, method = "dpll", multiple = True):
    if method == "dpll":
        logic = Logic(parse_logic(formula))
        return dpll_solve(logic, multiple = multiple)
    else:
        logic = parse_logic(formula)
        return robdd_solve(logic, multiple = multiple)