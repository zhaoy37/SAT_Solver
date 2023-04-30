"""

"""
import sys
sys.path.append('..')
from bdd.robdd_logic_generate import *
from bdd.robdd_solver import solve
from bdd.logic_eval import logic_eval_dict
from shared.logic_parser import parse_logic
import time
import numpy as np


def perform_ablation_study(num_formula=2, num_variables=3, depth=3, multiple=True):
    print("-----------------------------------------------------------------------------------")
    print("Evaluating ROBDD Solver (Ablation study):")
    print("Generating {} random logic with {} variables, depth={}...".format(num_formula, num_variables, depth))
    
    formulae = []
    single_logics = []
    for i in range(num_formula):
        single_logic = random_logic_gen(n=num_variables, components=depth)
        single_logics.append(single_logic)
        parsed = parse_logic(single_logic)
        formulae.append(parsed)
    print("Success.")
    
    print("Evaluating multiple solutions:", bool(multiple))

    # Now solve the trees with different capabilities:
    print("Test the solving time with no heuristic and no heuristic enabled:")
    
    solutions = []
    for logic in formulae:
        if multiple:
            sol, elp_time = solve(logic, get_time=True, multiple=True)
            solutions.append(sol)
        else:
            sol, elp_time = solve(logic, get_time=True, multiple=False)
            if sol!="UNSAT":
                solutions.append(sol[0])
            else:
                solutions.append("UNSAT")
    print("Execution time: %s seconds" % elp_time)

    # Now evaluate the accuracy.
    if not multiple:
        print("Evaluating the accuracy (This only evaluates the accuracy on problems that are SAT, for a more complete version, use Z3 to prove UNSAT):")
        correct_num = 0
        total = 0
        for i in range(len(formulae)):
            if solutions[i] != "UNSAT":
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
                    if int(logic_eval_dict(formulae[i], single_sol)) != 1:
                        print(logic_eval_dict(formulae[i], single_sol), single_logics[i], single_sol)
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
    for i in range(num_formula):
        single_logic = random_logic_gen(n=num_variables, components=depth)
        parsed = parse_logic(single_logic)
        formulae.append(parsed)
    print("Success.")

    # Now solve the trees with different capabilities:
    print("Test the solving time with no heuristic and no heuristic enabled:")
    
    single_solutions = []
    multi_solutions = []
    for logic in formulae:
        sol, elp_time = solve(logic, get_time=True, multiple=True)
        if sol!="UNSAT":
            single_solutions.append(sol[0])
            multi_solutions.append(sol)
        else:
            single_solutions.append("UNSAT")
            multi_solutions.append("UNSAT")


    print("Execution time: %s seconds" % elp_time)

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
    ## test
    # formula = "(((x2 and x0) and (x0 or x2)) or (((not x2) and x1) or (x2 and x2)))"
    # parsed = parse_logic(formula)
    # sol, elp_time = solve(parsed, get_time=True, multiple=True)
    # print(sol)
    # for single_sol in sol:
    #     if int(logic_eval_dict(parsed, single_sol)) != 1:
    #         print('wrong')
    #     print(logic_eval_dict(parsed, single_sol), parsed, single_sol)


    perform_ablation_study(100, 3, 3, False)
    perform_ablation_study(100, 3, 3, True)
    cross_check(100)