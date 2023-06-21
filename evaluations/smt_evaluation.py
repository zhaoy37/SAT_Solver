"""
Author(s): Yiqi (Nick) Zhao

In this file, I evaluate and compare the SMT solver kernels.
"""

from resources.smt_clause_generator import *
from SMT_Solver.smt import solve_SMT
import time

def evaluate_smt_kernel(kernel_name, random_smt_logics):
    """
    This function evaluates one specific kernel given the kernel name.
    """
    print("Evaluating Kernel", kernel_name)
    print("Solving begin")
    solving_begin = time.time()
    solutions = []
    for smt_logic in random_smt_logics:
        sat_formula, encodings, smt_vars, lowerbound, upperbound = smt_logic
        solutions.append(solve_SMT(sat_formula, encodings, smt_vars, lowerbound, upperbound, method = kernel_name))
    solving_time = time.time() - solving_begin
    print("Solving ends after %s seconds", solving_time)

    # Evaluate the accuracy of the solutions.
    
    return solutions



def perform_smt_evaluation(num_clauses, num_sat_variables, num_smt_variables, depth_sat, lower_bound, upper_bound):
    # First, generate the random smt logics.
    #Todo: include "robdd" kernel later after I improve it.
    random_smt_logics = generate_random_SMT_clauses(num_clauses, num_sat_variables, num_smt_variables, depth_sat, lower_bound, upper_bound)
    for kernel in ["backtracking", "minconflicts"]:
        evaluate_smt_kernel(kernel, random_smt_logics)


if __name__ == "__main__":
    perform_smt_evaluation(10, 2, 2, 2, 0, 10)

