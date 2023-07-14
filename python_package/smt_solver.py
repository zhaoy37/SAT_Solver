from .smt import solve_SMT
from .smt_parser import parse_smt

def smt_solve(formula, lower_bound, upper_bound, method = "backtracking"):
    converted = parse_smt(formula)
    sat_formula, smt_formula, smt_vars = converted
    solution = solve_SMT(sat_formula, smt_formula, smt_vars, lower_bound, upper_bound, method=method)
    return solution