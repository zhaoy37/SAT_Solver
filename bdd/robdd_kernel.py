from shared.logic_parser import parse_logic
from bdd.rodbb_plot import view_rodbb
from bdd.robdd_graph import ROBDD_graph
from bdd.robdd_solver import convert_robdd_graph, construct_obdd, robddPaths
import pprint
import time



def robdd_kernel():
    print("Running ROBDD solver.")
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
        print("For example, try: ((x0 and x1) or ((not x0) and (not x1)))")
        formula = input("Please enter the formula here (literal must starts with x and followed by numbers):")
    else:
        print("Testing pre-defined logic expression:", end=" ")
        formula = "((x0 or (not x1)) and (x1 or x2))"
        logic = parse_logic(formula)
        print(formula)
        print("Testing pre-defined variable ordering: x2, x1, x0")
        ordering = [2, 1, 0]
        obdd = construct_obdd(ordering, logic, vis=True)
        print("Testing pre-defined variable ordering: x0, x1, x2")
        ordering = [0, 1, 2]   ## tree will be constructed in the order of x0, x1, x2
        obdd = construct_obdd(ordering, logic, vis=True)
        
        print("Converting OBDD to ROBDD using graph representation.")
        g = ROBDD_graph(directed=True)
        robdd_res = convert_robdd_graph(obdd, g)
        g.reduce()
        print("View result:")
        robddPaths(g)
        print("Plot result:")
        view_rodbb(g)



def test():
    robdd_kernel()