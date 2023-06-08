"""
Authors: Yiqi (Nick) Zhao
The main file evaluates the dpll solver created.

Acknowledgement:
I used: https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-executi
"""

# Import necessary modules.
from resources.logic_generator import generate_logic_trees
from dpll.solver import solve

# Time some executions following this link:
import time
import numpy as np

def perform_ablation_study(num_formula, num_variables, depth, multiple):
    print("Evaluating the DPLL Solver (Ablation study):")
    print("-------------------------------------")
    print("Generating random trees:")
    trees = []
    num_nodes = []
    for i in range(num_formula):
        tree2 = generate_logic_trees(1, num_variables, depth)[0]
        num_nodes.append(tree2.num_of_nodes())
        trees.append(tree2)
    print("User specified values:")
    print("The number of formula(e):", num_formula)
    print("The depth of each tree:", depth)
    print("The mode of multiple solutions:", bool(multiple))
    print()
    print("Framework generated values:")
    print("The average number of nodes for each tree is:", np.average(num_nodes))
    print("The maximum number of nodes is:", max(num_nodes))
    print("The minimum number of nodes is:", min(num_nodes))
    print("-------------------------------------")

    # Now solve the trees with different capabilities:
    print("-------------------------------------")
    print("Test the solving time with no heuristic and no heuristic enabled:")
    no_assignment = time.time()
    single_noh_solutions = []
    multiple_noh_solutions = []
    for tree in trees:
        if multiple:
            multiple_noh_solutions.append(solve(tree, heuristic_enabled = False, multiple = True))
        else:
            single_noh_solutions.append(solve(tree, heuristic_enabled = False, multiple = False))
    print("Execution with no heuristic: %s seconds" % (time.time() - no_assignment))
    print("-------------------------------------")

    print("-------------------------------------")
    print("Test the solving time with heuristic enabled:")
    assignment = time.time()
    single_h_solutions = []
    multiple_h_solutions = []
    for tree in trees:
        if multiple:
            multiple_h_solutions.append(solve(tree, heuristic_enabled=True, multiple=True))
        else:
            single_h_solutions.append(solve(tree, heuristic_enabled=True,  multiple=False))
    print("Execution with heuristic: %s seconds" % (
                time.time() - assignment))
    print("-------------------------------------")

    # Now evaluate the accuracy.
    print()
    if not multiple:
        print("Evaluating the accuracy (This only evaluates the accuracy on problems that are SAT, for a more complete version, use Z3 to prove UNSAT):")
        print("-------------------------------------")
        correct_num = 0
        total = 0
        for i in range(len(trees)):
            if single_noh_solutions[i] != "UNSAT":
                correct_num += trees[i].evaluate(single_noh_solutions[i])
                total += 1
        print("Accuracy for No Heuristic:", correct_num * 100 / total, "%")

        correct_num = 0
        total = 0
        for i in range(len(trees)):
            if single_h_solutions[i] != "UNSAT":
                correct_num += trees[i].evaluate(single_h_solutions[i])
                total += 1
        print("Accuracy for Heuristic:", correct_num * 100 / total, "%")
    else:
        print("Evaluating the accuracy (This only evaluates the accuracy on problems that are SAT, for a more complete version, use Z3 to prove UNSAT):")
        print("-------------------------------------")
        correct_num = 0
        total = 0
        for i in range(len(trees)):
            if multiple_noh_solutions[i] != "UNSAT":
                for j in range(len(multiple_noh_solutions[i])):
                    correct_num += trees[i].evaluate(multiple_noh_solutions[i][j])
                    total += 1
        print("Accuracy for No Heuristic:", correct_num * 100 / total, "%")

        correct_num = 0
        total = 0
        for i in range(len(trees)):
            if multiple_h_solutions[i] != "UNSAT":
                for j in range(len(multiple_noh_solutions[i])):
                    correct_num += trees[i].evaluate(multiple_h_solutions[i][j])
                    total += 1
        print("Accuracy for Heuristic:", correct_num * 100 / total, "%")

        print()
        print("Cross checking the completeness of solutions:")
        print("-------------------------------------")
        correct_num = 0
        total = 0
        for i in range(len(multiple_noh_solutions)):
            if multiple_noh_solutions[i] != "UNSAT":
                correct_num += (len(multiple_noh_solutions[i]) == len(multiple_h_solutions[i]))
                total += 1
        print("Accuracy on completeness of all possible solutions:", correct_num * 100 / total, "%")


if __name__ == "__main__":
    perform_ablation_study(1000, 3, 5, False)