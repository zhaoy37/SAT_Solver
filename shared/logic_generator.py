"""
Author: Yiqi (Nick) Zhao

This file allows random generations of logics.
"""

from numpy import random
from dpll.logic_tree import Logic

"""
The following functions should not be exposed to public if used for packages,
because they may raise confusions due to the complex method names.
"""

"""
This function generates one logic (in a formula format).
"""
def generate_one_logic(num_possible_variables, depth):
    # Obtain possible leaves.
    leaves = ["x" + str(i) for i in range(num_possible_variables)]
    if depth < 0:
        raise Exception("Depth too low for generating a logic.")
    elif depth == 0:
        return leaves[random.randint(0, len(leaves))]
    else:
        if random.randint(0, 3) == 0:
            return ["not", generate_one_logic(num_possible_variables, depth - 1)]
        elif random.randint(0, 3) == 1:
            return ["and", generate_one_logic(num_possible_variables, depth - 1),
                    generate_one_logic(num_possible_variables, depth - 1)]
        else:
            return ["or", generate_one_logic(num_possible_variables, depth - 1),
                    generate_one_logic(num_possible_variables, depth - 1)]


"""
This function generates some logics using a random generator (in a formula format).
"""
def generate_logics(num_logics, num_possible_variables, depth):
    logics = []
    for i in range(num_logics):
        if depth == 0:
            logics.append([generate_one_logic(num_possible_variables, depth)])
        else:
            logics.append(generate_one_logic(num_possible_variables, depth))
    return logics


"""
This function generates random logic trees for DPLL.
"""
def generate_random_logic_trees(num_logics, num_possible_variables, depth):
    formulae = generate_logics(num_logics, num_possible_variables, depth)
    return [Logic(formula = formula) for formula in formulae]


"""
This function generates random logic trees for DPLL with forced number of variables.
"""
def generate_random_logic_trees_forced_numvariables(num_logics, num_variables, depth):
    logics = []
    while len(logics) < num_logics:
        logic = generate_one_logic(num_variables, depth)
        tree = Logic(logic)
        if len(tree.leaves) == num_variables:
            logics.append(tree)
    return logics


"""
This function generates random logic trees for DPLL with forced number of variables with no repetations.
"""
def generate_random_logic_trees_forced_numvariables_no_repetation(num_logics, num_variables, depth):
    logics = set()
    while len(logics) < num_logics:
        logic = generate_one_logic(num_variables, depth)
        tree = Logic(logic)
        if len(tree.leaves) == num_variables:
            logics.add(tree)
    return list(logics)