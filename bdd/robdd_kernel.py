"""
Authors: Ziyan An
References: 

Implementations for input prompts and user interactions.
"""

from shared.logic_parser import parse_logic
from bdd.rodbb_visualization import view_rodbb
from bdd.robdd_graph import ROBDD_graph
from bdd.robdd_solver import *
from bdd.robdd_logic_generate import *
import pprint
import time



def user_prompt_generat_formulae():
    # asks for user input
    num_param = input("Enter the number of variables:")
    while not num_param.isnumeric():
        num_param = input("Invalid input. Please re-enter:")
    num_param = int(num_param)
    num_comp = input("Enter the number of logic components (`x0 and x1` is a component):")
    while (not num_comp.isnumeric()) and (not int(num_comp)>=(num_param)):
        num_comp = input("Invalid input. Please re-enter:")
    num_comp = int(num_comp)
    gen_logic = random_logic_gen(n=num_param, components=num_comp)
    return gen_logic, num_param, num_comp



def robdd_kernel():
    print("Running ROBDD solver.")
    print("Do you want to:  1. specify the formula(e) or \n \
          \t 2. test the solver on pre-generated formula(e) or \n \
          \t 3. test the solver on randomly generated formula(e)")
    print("-----------------------------------------------------------------------------------")
    choice = input("Enter the input here:")
    while not choice.isnumeric() or (not (int(choice) <= 3)):
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
        print("Creating graph representation.")
        G = view_rodbb(g, ordering)


    elif int(choice) == 2:
        print("Testing pre-defined logic expression:", end=" ")
        # formula = "((x0 or (not x1)) and (x1 or x2))"
        formula = "(((not x0) and (not x1) and (not x2)) or (x0 and x1) or (x1 and x2))"
        formula = "(((x2 and x2) or (x0 and (not x1))) or ((x1 or (not x0)) and (x0 or x1)))"
        # formula = "(x0 and x1) or (x2 and x3) or (x4 and x5) or (x6 and x7)"
        logic = parse_logic(formula)
        print("Your logic formula:", formula)
        print("-----------------------------------------------------------------------------------")

        ## robdd is tested on two orderings for the formula. 
        ## results should be the same.
        print("Testing pre-defined variable ordering: ", end='')
        # ordering = [0, 2, 4, 6, 1, 3, 5, 7]
        ordering = [0, 1, 2]
        print(ordering)
        obdd = construct_obdd(ordering, logic, vis=True)

        ## converting obdd in the tree structure to robdd as a graph.
        print("Converting OBDD to ROBDD using graph representation.")
        g = ROBDD_graph(directed=True, init_val=ordering[0])
        robdd_res = convert_robdd_graph(obdd, g)
        g.reduce()
        # print("View result:")
        # robddPaths(g)
        print("Creating graph representation.")
        G = view_rodbb(g, ordering)
        
        print("-----------------------------------------------------------------------------------")
        print("Testing pre-defined variable ordering: ", end='')
        # ordering = [0, 1, 2, 3, 4, 5, 6, 7]   ## tree will be constructed in the order of x0, x1, x2
        ordering = [2, 1, 0]
        print(ordering)
        obdd = construct_obdd(ordering, logic, vis=True)
        
        ## converting obdd in the tree structure to robdd as a graph.
        print("Converting OBDD to ROBDD using graph representation.")
        g = ROBDD_graph(directed=True, init_val=ordering[0])
        robdd_res = convert_robdd_graph(obdd, g)
        g.reduce()
        # print("View result:")
        # robddPaths(g)
        print("Creating graph representation.")
        G = view_rodbb(g, ordering)
        

    elif int(choice) == 3:
        print("Testing a randomly generated logic formula.")
        formula, num_param, _ = user_prompt_generat_formulae()
        logic = parse_logic(formula)
        print("Generated logic formula:", formula)

        print("Please enter the ordering of parameters.")
        user_input = input("For example, enter `0 1 2` for the order (x0, x1, x2):")
        try:
            ordering = [int(n) for n in user_input.split()]
        except:
            raise ValueError("Unauthorized text:", user_input)
        if len(ordering) < num_param:
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
        print("Creating graph representation.")
        G = view_rodbb(g, ordering)


    print("--------------------------------------Done.----------------------------------------")



def test():
    robdd_kernel()