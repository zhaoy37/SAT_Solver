"""
Author(s): Yiqi (Nick) Zhao

In this file, I evaluate and compare the SMT solver kernels.
"""
import sys
sys.path.insert(0, '..')
from resources.smt_clause_generator import *
from SMT_Solver.smt import solve_SMT
from resources.calculator import calculate
import time


def verify_solution(solution, sat_formula, smt_formula):
    sat_valuations = dict()
    for sat_atom in smt_formula:
        formula = smt_formula[sat_atom]
        try:
            var1 = calculate(formula[1], solution)
            var2 = calculate(formula[2], solution)
        except ZeroDivisionError:
            sat_valuations[sat_atom] = False
            continue

        operator = formula[0]
        # Perform checking.
        sat_flag = True
        if operator == "lt":
            if var1 >= var2:
                sat_flag = False
        elif operator == "gt":
            if var1 <= var2:
                sat_flag = False
        elif operator == "ge":
            if var1 < var2:
                sat_flag = False
        elif operator == "le":
            if var1 > var2:
                sat_flag = False
        elif operator == "eq":
            if var1 != var2:
                sat_flag = False
        else:
            if var1 == var2:
                sat_flag = False
        sat_valuations[sat_atom] = sat_flag
    return Logic(sat_formula).evaluate(sat_valuations)


def evaluate_smt_kernel(kernel_name, random_smt_logics):
    """
    This function evaluates one specific kernel given the kernel name.
    """
    print("Evaluating Kernel:", kernel_name)
    print("Solving begin.")
    solving_begin = time.time()
    solutions = []
    for i in range(len(random_smt_logics)):
        sat_formula, encodings, smt_vars, lowerbound, upperbound = random_smt_logics[i]
        solutions.append(solve_SMT(sat_formula, encodings, smt_vars, lowerbound, upperbound, method = kernel_name))
    solving_time = time.time() - solving_begin
    print(f"Solving ends after {solving_time} seconds.")

    # Evaluate the accuracy of the solutions.
    print("Check the accuracy of the solutions for Kernel:", kernel_name)
    print("Check Accuracy for SAT solutions:")
    correct_count = 0
    total_count = 0
    for i in range(len(solutions)):
        if solutions[i] != "UNSAT":
            correct_count += verify_solution(solutions[i], random_smt_logics[i][0], random_smt_logics[i][1])
            total_count += 1
    print("The correctness is:", correct_count / total_count)
    return solutions



def perform_smt_evaluation(num_clauses, num_sat_variables, num_smt_variables, depth_sat, lower_bound, upper_bound):
    # First, generate the random smt logics.
    random_smt_logics = generate_random_SMT_clauses(num_clauses, num_sat_variables, num_smt_variables, depth_sat, lower_bound, upper_bound)
    all_solutions = []
    for kernel in ["backtracking", "minconflicts", "robdd"]:
        all_solutions.append(evaluate_smt_kernel(kernel, random_smt_logics))
    # Now, perform cross_check for UNSAT.
    print("Check Accuracy for UNSAT solutions:")
    UNSAT_correctness_flag = True
    for j in range(len(all_solutions[0])):
        if all_solutions[0][j] == "UNSAT":
            for i in range(len(all_solutions)):
                if all_solutions[i][j] != "UNSAT":
                    print("Problem Detected for UNSAT Checking")
                    UNSAT_correctness_flag = False

    if UNSAT_correctness_flag:
        print("The correctness for UNSAT checking is 100%")


if __name__ == "__main__":
    perform_smt_evaluation(10, 2, 2, 2, -10, 10)

