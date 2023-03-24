"""
Author: Yiqi Zhao

This file controls different interface and constructs a single
kernel for the users.
"""

from dpll.dpll_kernel import dpll_kernel

def main():
    print("Thank you for using EduSATSolver. Please select what you want to do from the following options.")
    print("-----------------------------------------------------------------------------------")
    print("1. Play with the solver we created.")
    print("2. Use an SMT solver to solve some interesting problems.")
    print("-----------------------------------------------------------------------------------")
    selection = input("Enter your selection here:")
    while not selection.isnumeric() or (not (int(selection) == 1 or int(selection) == 2)):
        selection = input("Invalid input. Please re-enter:")
    print()
    if int(selection) == 1:
        dpll_kernel()
    else:
        print("For instructions on using an SMT solver for some interesting problems, please see the README file")
        print("(and our report if you want to know more details of how some problems are solved.)")

if __name__ == "__main__":
    main()