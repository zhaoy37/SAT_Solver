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
    print("Test the solving time with no tree heuristic and no assignment heuristic enabled:")
    no_tree_no_assignment = time.time()
    for tree in trees:
        if multiple:
            solve(tree, assignment_heuristic_enabled = False, tree_heuristic_enabled = False, multiple = True)
        else:
            solve(tree, assignment_heuristic_enabled = False, tree_heuristic_enabled = False, multiple = False)
    print("Execution with no tree heuristic and no assignment heuristic: %s seconds" % (time.time() - no_tree_no_assignment))
    print("-------------------------------------")

    print("-------------------------------------")
    print("Test the solving time with no tree heuristic but assignment heuristic enabled:")
    no_tree_assignment = time.time()
    for tree in trees:
        if multiple:
            solve(tree, assignment_heuristic_enabled=True, tree_heuristic_enabled=False, multiple=True)
        else:
            solve(tree, assignment_heuristic_enabled=True, tree_heuristic_enabled=False, multiple=False)
    print("Execution with no tree heuristic but with assignment heuristic: %s seconds" % (
                time.time() - no_tree_assignment))
    print("-------------------------------------")


    print("-------------------------------------")
    print("Test the solving time with tree heuristic but no assignment heuristic enabled:")
    tree_no_assignment = time.time()
    for tree in trees:
        if multiple:
            solve(tree, assignment_heuristic_enabled=False, tree_heuristic_enabled=True, multiple=True)
        else:
            solve(tree, assignment_heuristic_enabled=False, tree_heuristic_enabled=True, multiple=False)
    print("Execution with tree heuristic but no assignment heuristic: %s seconds" % (
                time.time() - tree_no_assignment))
    print("-------------------------------------")

    print("-------------------------------------")
    print("Test the solving time with both tree heuristic and assignment heuristic enabled:")
    tree_assignment = time.time()
    for tree in trees:
        if multiple:
            solve(tree, assignment_heuristic_enabled=True, tree_heuristic_enabled=True, multiple=True)
        else:
            solve(tree, assignment_heuristic_enabled=True, tree_heuristic_enabled=True, multiple=False)
    print("Execution with both tree heuristic and assignment heuristic: %s seconds" % (
            time.time() - tree_assignment))
    print("-------------------------------------")


if __name__ == "__main__":
    perform_ablation_study(10000, 3, 5, False)