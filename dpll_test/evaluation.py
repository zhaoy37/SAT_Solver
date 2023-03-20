"""
Authors: Yiqi (Nick) Zhao
The main file evaluates the dpll solver created.

Acknowledgement:
I used: https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-executi
"""

# Import necessary modules.
from dpll.logic_tree import Logic
from shared.logic_parser import parse_logic
from shared.logic_generator import generate_logic_trees
from dpll.solver import naive_solve

# Time some executions following this link:
import time

def perform_intrasolver_test_single_formula_single_solution(num_variables, depth):

    # To set the hyperparameter in controlling the percentage
    # of and, or, not nodes, please refer to solver.py.

    print("This program tests the ability of the created SAT solver:")
    print()
    tree2 = generate_logic_trees(1, num_variables, depth)[0]
    print("A randomly generated tree is:")
    print(tree2.formula)

    print("The total number of nodes are:")
    print(tree2.num_of_nodes())
    print()

    noheuristic = time.time()
    solution = naive_solve(tree2, tree_heuristic_enabled = False)
    print("---Execution with no Heuristic (naive): %s seconds --- " % (time.time() - noheuristic))
    print(solution)

    heuristic = time.time()
    solution = naive_solve(tree2, tree_heuristic_enabled = True)
    print("---Execution with heurisitc (naive): %s seconds --- " % (time.time() - heuristic))
    print(solution)

    if(solution != "UNSAT"):
        print("---Is the results correct?---")
        print(bool(tree2.evaluate(solution)))


if __name__ == "__main__":
    # Change the function to be called for evaluation here.
    perform_intrasolver_test_single_formula_single_solution(num_variables = 10, depth = 5)