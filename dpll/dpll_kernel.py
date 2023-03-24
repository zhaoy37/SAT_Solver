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
from dpll.solver import solve

# Time some executions following this link:
import time


def test_on_randomly_generated_formulae():
    # Ask for user input.
    num_formula = input("Enter the number of formulae to test on:")
    while not num_formula.isnumeric():
        num_formula = input("Invalid input. Please re-enter:")
    num_formula = int(num_formula)
    user_num_variables = input("Enter the number of variables for each formula:")
    while not user_num_variables.isnumeric():
        user_num_variables = input("Invalid input. Please re-enter:")
    user_num_variables = int(user_num_variables)
    tree_depth = input("Enter the depth of tree for each formula:")
    while not tree_depth.isnumeric():
        tree_depth = input("Invalid input. Please re-enter:")
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
    print("---Timer Started---")
    print("---Solving the tree---")
    for i in range(len(trees)):
        tree = trees[i]
        solution = solve(tree)
        print("Solving tree", i + 1)
        print(solution)
    print("---Total time to find the solution(s): %s seconds --- " % (time.time() - start_time))


def dpll_kernel():
    print("Running the DPLL solver.")
    print("Do you want to 1. specify the formula(e) or 2. test the solver on randomly generated formula(e)?")
    print("-------------------------------------------------------------")
    choice = input("Enter the input here:")
    while not choice.isnumeric() or (not (int(choice) == 1 or int(choice) == 2)):
        choice = input("Invalid input. Please re-enter:")
    print("-------------------------------------------------------------")

    if int(choice) == 1:
        print("Please enter the formula following the syntax below: ")
        print("<formula> := True | False | literal | <formula> and <formula>")
        print("| <formula> or <formula> | not <formula> |")
        print("(<formula>)")
        formula = input("Please enter the formula here (literal must starts with x and followed by numbers):")
        logic = Logic(parse_logic(formula))
        print()
        print("Do you want to see only one solution or all solutions?")
        print("Enter 1 to see only 1 solution.")
        print("Enter 2 to see all solutions.")
        print()
        solution_choice = input("Enter your choice here:")
        while not solution_choice.isnumeric() or (not (int(solution_choice) == 1 or int(solution_choice) == 2)):
            solution_choice = input("Invalid input. Please re-enter:")
        start_time = time.time()
        print("---Timer started---")
        if int(solution_choice) == 1:
            solution = solve(logic)
            print("The solution is:", solution)
        else:
            solutions = solve(logic, multiple = True)
            print("The solution(s) is/are:")
            for s in solutions:
                print(s)
        print("---Total time to find the solution(s): %s seconds --- " % (time.time() - start_time))
    else:
        # Case 2: Test the solver on randomly generated formula(e).
        test_on_randomly_generated_formulae()
