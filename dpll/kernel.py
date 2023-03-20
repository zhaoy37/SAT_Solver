"""
Authors: Yiqi (Nick) Zhao

The main file gives an interface to the dpll.

Acknowledgement:
I used: https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-executi
"""

# Import necessary modules.
from dpll.logic_tree import Logic
from shared.logic_parser import parse_logic
from shared.logic_generator import generate_logic_trees
from solver import naive_solve

# Time some executions following this link:
import time


def test_on_randomly_generated_formulae():
    # Ask for user input.
    print("Enter the number of formulae to test on:")
    num_formula = input()
    while not num_formula.isnumeric():
        print("Invalid input. Please re-enter:")
        num_formula = input()
    num_formula = int(num_formula)
    print("Enter the number of variables for each formula:")
    user_num_variables = input()
    while not user_num_variables.isnumeric():
        print("Invalid input. Please re-enter:")
        user_num_variables = input()
    user_num_variables = int(user_num_variables)
    print("Enter the depth of tree for each formula:")
    tree_depth = input()
    while not tree_depth.isnumeric():
        print("Invalid input. Please re-enter:")
        tree_depth = input()
    tree_depth = int(tree_depth)

    # To set the hyperparameter in controlling the percentage
    # of and, or, not nodes, please refer to solver.py.
    print("--------------------------")
    print("Testing the ability of the created SAT solver:")
    print()
    print("Generating trees.")
    trees = []
    for i in range(num_formula):
        tree = generate_logic_trees(1, num_variables = user_num_variables, depth = tree_depth)[0]
        trees.append(tree)
        print("A randomly generated tree is:")
        print(tree.formula)

        print("The total number of nodes are:")
        print(tree.num_of_nodes())
        print()

    start_time = time.time()
    print("---Solving the tree---")
    for i in range(len(trees)):
        tree = trees[i]
        solution = naive_solve(tree)
        print("Solving tree", i + 1)
        print(solution)
    print("---Total time to find the solution(s): %s seconds --- " % (time.time() - start_time))


def main():
    print("Running the DPLL solver.")
    print("Do you want to 1. specify the formula(e) or 2. test the solver on randomly generated formula(e)?")
    print("-------------------------------------------------------------")
    print("Enter the input here:")
    choice = input()
    while not choice.isnumeric() or (not (int(choice) == 1 or int(choice) == 2)):
        print("Invalid input. Please re-enter:")
        choice = input()
    print("-------------------------------------------------------------")

    if int(choice) == 1:
        pass
    else:
        # Case 2: Test the solver on randomly generated formula(e).
        test_on_randomly_generated_formulae()


if __name__ == "__main__":
    main()

