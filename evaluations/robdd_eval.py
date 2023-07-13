"""

"""
import sys
sys.path.append('..')
from resources.logic_generator import generate_one_logic
from bdd.robdd_solver import solve
from bdd.logic_eval import logic_eval_dict
from resources.logic_parser import parse_logic
import time
import random
import numpy as np
random.seed(0)


def perform_ablation_study(num_formula=2, num_variables=3, depth=3, multiple=True):
    print("-----------------------------------------------------------------------------------")
    print("Evaluating ROBDD Solver (Ablation study):")
    print("Generating {} random logic with {} variables, depth={}...".format(num_formula, num_variables, depth))
    
    formulae = []
    # single_logics = []
    for i in range(num_formula):
        # single_logic = random_logic_gen(n=num_variables, components=depth)
        # single_logics.append(single_logic)
        parsed = generate_one_logic(num_variables, depth, False)
        formulae.append(parsed)
    print("Success.")
    
    print("Evaluating multiple solutions:", bool(multiple))

    # Now solve the trees with different capabilities:
    
    solutions = []
    total_time = 0
    for logic in formulae:
        if multiple:
            sol, elp_time = solve(logic, get_time=True, multiple=True)
            solutions.append(sol)
            total_time += elp_time
        else:
            sol, elp_time = solve(logic, get_time=True, multiple=False)
            total_time += elp_time
            if sol!="UNSAT":
                solutions.append(sol[0])
            else:
                solutions.append("UNSAT")
    print("Execution time: %s seconds" % total_time)

    # Now evaluate the accuracy.
    if not multiple:
        print("Evaluating the accuracy (This only evaluates the accuracy on problems that are SAT, for a more complete version, use Z3 to prove UNSAT):")
        correct_num = 0
        total = 0
        for i in range(len(formulae)):
            if solutions[i] != "UNSAT":
                # if int(logic_eval_dict(formulae[i], solutions[i])) != 1:
                #     print(logic_eval_dict(formulae[i], solutions[i], verbose=True), single_logics[i], solutions[i])
                correct_num += logic_eval_dict(formulae[i], solutions[i])
                total += 1
        if total != 0:
            print("ACCURACY:", correct_num * 100 / total, "%")
        else:
            print("ACCURACY: UNSAT")

    else:
        print("Evaluating the accuracy (This only evaluates the accuracy on problems that are SAT, for a more complete version, use Z3 to prove UNSAT):")
        correct_num = 0
        total = 0
        for i in range(len(formulae)):
            if solutions[i] != "UNSAT":
                for single_sol in solutions[i]:
                    # if int(logic_eval_dict(formulae[i], single_sol)) != 1:
                        # print(logic_eval_dict(formulae[i], single_sol, verbose=True), single_logics[i], single_sol)
                    correct_num += int(logic_eval_dict(formulae[i], single_sol))
                    total += 1
        if total != 0:
            print("ACCURACY:", correct_num * 100 / total, "%")
        else:
            print("ACCURACY: UNSAT")
    print("-----------------------------------------------------------------------------------")




def cross_check(num_formula=2, num_variables=3, depth=3):
    print("-----------------------------------------------------------------------------------")
    print("Evaluating ROBDD Solver (cross check):")
    print("Generating {} random logic with {} variables, depth={}...".format(num_formula, num_variables, depth))
    
    formulae = []
    # single_logics = []
    for i in range(num_formula):
        # single_logic = random_logic_gen(n=num_variables, components=depth)
        # single_logics.append(single_logic)
        parsed = generate_one_logic(num_variables, depth, False)
        formulae.append(parsed)
    print("Success.")

    # Now solve the trees with different capabilities:
    print("Test the solving time with no heuristic and no heuristic enabled:")
    
    single_solutions = []
    multi_solutions = []
    total_time = 0
    for idx,logic in enumerate(formulae):
        sol, elp_time = solve(logic, get_time=True, multiple=True)
        total_time += elp_time
        if sol!="UNSAT":
            try:
                single_solutions.append(sol[0])
                multi_solutions.append(sol)
            except:
                continue
        else:
            single_solutions.append("UNSAT")
            multi_solutions.append("UNSAT")

    print("Execution time: %s seconds" % total_time)

    # Now evaluate the accuracy.
    print("Cross checking the completeness of solutions:")
    correct_num = 0
    total = 0
    for i in range(len(multi_solutions)):
        if single_solutions[i] != "UNSAT":
            correct_num += (len(multi_solutions[i]) >= 1)
            total += 1
    if total != 0:
        print("ACCURACY on completeness:", correct_num * 100 / total, "%")
    else:
        print("ACCURACY: UNSAT")
    print("-----------------------------------------------------------------------------------")



if __name__ == "__main__":

    ## testing on more logic formulae
    perform_ablation_study(1, 3, 3, False)
    perform_ablation_study(1, 3, 3, True)
    cross_check(1)

    perform_ablation_study(10, 3, 3, False)
    perform_ablation_study(10, 3, 3, True)
    cross_check(10)

    perform_ablation_study(50, 3, 3, False)
    perform_ablation_study(50, 3, 3, True)
    cross_check(50)

    perform_ablation_study(100, 3, 3, False)
    perform_ablation_study(100, 3, 3, True)
    cross_check(100)

    perform_ablation_study(500, 3, 3, False)
    perform_ablation_study(500, 3, 3, True)
    cross_check(500)

    perform_ablation_study(1000, 3, 3, False)
    perform_ablation_study(1000, 3, 3, True)
    cross_check(1000)

    ## testing on more logic components 
    # perform_ablation_study(10, 5, 5, False)
    # perform_ablation_study(10, 5, 5, True)
    # cross_check(10, 5, 5)

    # perform_ablation_study(10, 5, 5, False)
    # perform_ablation_study(10, 5, 5, True)
    # cross_check(10, 5, 5)

    # perform_ablation_study(10, 5, 6, False)
    # perform_ablation_study(10, 5, 6, True)
    # cross_check(10, 5, 6)

    # perform_ablation_study(10, 5, 7, False)
    # perform_ablation_study(10, 5, 7, True)
    # cross_check(10, 5, 7)

    # ## testing on more variables
    # perform_ablation_study(10, 2, 1, False)
    # perform_ablation_study(10, 2, 1, True)
    # cross_check(10, 2, 1)

    # perform_ablation_study(10, 3, 3, False)
    # perform_ablation_study(10, 3, 3, True)
    # cross_check(10, 3, 3)

    # perform_ablation_study(10, 5, 7, False)
    # perform_ablation_study(10, 5, 7, True)
    # cross_check(10, 5, 7)

    # perform_ablation_study(10, 7, 6, False)
    # perform_ablation_study(10, 7, 6, True)
    # cross_check(10, 7, 6)