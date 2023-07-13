"""
Author: Yiqi Zhao

In this file, I write a kernel to allow users to try out the SMT solver.

I used the codes from here:
https://stackoverflow.com/questions/1265665/how-can-i-check-if-a-string-represents-an-int-without-using-try-except
"""

from SMT_Solver.smt import solve_SMT
from resources.smt_parser import parse_smt
import time


def check_int(s):
    # I used the codes from here: https://stackoverflow.com/questions/1265665/how-can-i-check-if-a-string-represents-an-int-without-using-try-except
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()


def smt_kernel():
    lower_bound = input("Please enter the lower bound:")
    while not check_int(lower_bound):
        lower_bound = input("The lower bound must be an integer. Please re-enter:")
    lower_bound = int(lower_bound)

    upper_bound = input("Please enter the upper bound:")
    while not check_int(upper_bound):
        upper_bound = input("The upper bound must be an integer. Please re-enter:")
    upper_bound = int(upper_bound)

    formula = input("Please enter the SMT formula to be solved:")
    converted = parse_smt(formula)
    sat_formula, smt_formula, smt_vars = converted

    selected_method = input("Which SMT solver method do you want to use? 1. backtracking; 2. minconflicts. 3. robdd. Please enter 1 or 2 or 3.")
    while selected_method != "1" and selected_method != "2" and selected_method != "3":
        selected_method = input("Invalid option. Please re-enter.")

    start_time = time.time()
    if selected_method == "1":
        solution = solve_SMT(sat_formula, smt_formula, smt_vars, lower_bound, upper_bound, method = "backtracking")
    elif selected_method == "2":
        solution = solve_SMT(sat_formula, smt_formula, smt_vars, lower_bound, upper_bound, method = "minconflicts")
    else:
        solution = solve_SMT(sat_formula, smt_formula, smt_vars, lower_bound, upper_bound, method = "robdd")
    print("---Total time to find the solution(s): %s seconds --- " % (time.time() - start_time))
    print("The solution is:", solution)
