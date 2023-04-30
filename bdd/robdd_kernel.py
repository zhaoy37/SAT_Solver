"""
Authors: Ziyan An
References: 

Implementations for input prompts and user interactions.
"""

from shared.logic_parser import parse_logic
from bdd.rodbb_visualization import view_rodbb
from bdd.robdd_graph import ROBDD_graph
from bdd.robdd_solver import convert_robdd_graph, construct_obdd, robddPaths
from bdd.robdd_logic_generate import *
import pprint
import time



def robdd_kernel():
    print("Running ROBDD solver.")
    print("Do you want to:  1. specify the formula(e) or \n \
          \t 2. test the solver on pre-generated formula(e) or \n \
          \t 3. test the solver on randomly generated formula(e)?")
    print("-----------------------------------------------------------------------------------")
    choice = input("Enter the input here:")
    while not choice.isnumeric() or (not (int(choice) == 1 or int(choice) == 2)):
        choice = input("Invalid input. Please re-enter:")
    print("-----------------------------------------------------------------------------------")

    if int(choice) == 1:
        ## inputs must follow a pre-defined syntax.
        print("Please enter the formula following the syntax below: ")
        print("<formula> := True | False | literal | <formula> and <formula>")
        print("\t | <formula> or <formula> | not <formula> | (<formula>)")
        print("For example, try: ((x0 and x1) or ((not x0) and (not x1)))")
        formula = input("Please enter the formula here (literal must starts with x and followed by numbers):")
        logic = parse_logic(formula)
        print("Your logic formula:", formula)

        print("Please enter the ordering of parameters.")
        user_input = input("For example, enter `0 1 2` for the order (x0, x1, x2):")
        try:
            ordering = [int(n) for n in user_input.split()] 
        except:
            raise ValueError("Unauthorized text:", user_input)
        print("Your parameter ordering:", ordering)
        print("-----------------------------------------------------------------------------------")
        
        print("Building your ordered BDD with visualizations.")
        obdd = construct_obdd(ordering, logic, vis=True)
        
        print("-----------------------------------------------------------------------------------")
        ## converting obdd in the tree structure to robdd as a graph.
        print("Converting your ordered BDD to ROBDD with graph representation.")
        g = ROBDD_graph(directed=True)
        robdd_res = convert_robdd_graph(obdd, g)
        g.reduce()
        # print("View result:")
        # robddPaths(g)
        # print("Plot result:")
        view_rodbb(g)
        print("--------------------------------------Done.----------------------------------------")


    elif int(choice) == 2:
        print("Testing pre-defined logic expression:", end=" ")
        # formula = "((x0 or (not x1)) and (x1 or x2))"
        formula = "(((not x0) and (not x1) and (not x2)) or (x0 and x1) or (x1 and x2))"
        logic = parse_logic(formula)
        print("Your logic formula:", formula)
        print("-----------------------------------------------------------------------------------")

        ## robdd is tested on two orderings for the formula. 
        ## results should be the same.
        print("Testing pre-defined variable ordering: x2, x1, x0")
        ordering = [2, 1, 0]
        obdd = construct_obdd(ordering, logic, vis=True)
        print("Testing pre-defined variable ordering: x0, x1, x2")
        ordering = [0, 1, 2]   ## tree will be constructed in the order of x0, x1, x2
        obdd = construct_obdd(ordering, logic, vis=True)
        
        print("-----------------------------------------------------------------------------------")
        ## converting obdd in the tree structure to robdd as a graph.
        print("Converting OBDD to ROBDD using graph representation.")
        g = ROBDD_graph(directed=True)
        robdd_res = convert_robdd_graph(obdd, g)
        g.reduce()
        # print("View result:")
        # robddPaths(g)
        # print("Plot result:")
        view_rodbb(g)
        print("--------------------------------------Done.----------------------------------------")

    elif int(choice) == 3:
        pass


def test():
    robdd_kernel()