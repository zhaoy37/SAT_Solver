"""
Author: Yiqi (Nick) Zhao

This file allows random generations of logics.

It is primarily used for testing now, but we may
consider allow this to be a part of the interface/package.
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
def generate_one_logic(num_possible_variables, depth, allow_True_False):
    # Obtain possible leaves.
    leaves = ["x" + str(i) for i in range(num_possible_variables)]
    if(allow_True_False):
        leaves.append("True")
        leaves.append("False")
    if depth < 0:
        raise Exception("Depth too low for generating a logic.")
    elif depth == 0:
        return leaves[random.randint(0, len(leaves))]
    else:
        if random.randint(0, 3) == 0:
            return ["not", generate_one_logic(num_possible_variables, depth - 1, allow_True_False)]
        elif random.randint(0, 3) == 1:
            return ["and", generate_one_logic(num_possible_variables, depth - 1, allow_True_False),
                    generate_one_logic(num_possible_variables, depth - 1, allow_True_False)]
        else:
            return ["or", generate_one_logic(num_possible_variables, depth - 1, allow_True_False),
                    generate_one_logic(num_possible_variables, depth - 1, allow_True_False)]


"""
This function generates some logics using a random generator (in a formula format).
"""
def generate_logics(num_logics, num_possible_variables, depth, allow_True_False):
    logics = []
    for i in range(num_logics):
        if depth == 0:
            logics.append([generate_one_logic(num_possible_variables, depth, allow_True_False)])
        else:
            logics.append(generate_one_logic(num_possible_variables, depth, allow_True_False))
    return logics


"""
This function generates random logic trees for DPLL.
"""
def generate_random_logic_trees(num_logics, num_possible_variables, depth, allow_True_False):
    formulae = generate_logics(num_logics, num_possible_variables, depth, allow_True_False)
    return [Logic(formula = formula) for formula in formulae]


"""
This function generates random logic trees for DPLL with forced number of variables.
"""
def generate_random_logic_trees_forced_numvariables(num_logics, num_variables, depth, allow_True_False):
    logics = []
    while len(logics) < num_logics:
        logic = generate_one_logic(num_variables, depth, allow_True_False)
        tree = Logic(logic)
        if len(tree.leaves) == num_variables:
            logics.append(tree)
    return logics


"""
This function generates random logic trees for DPLL with forced number of variables with no repetations.
"""
def generate_random_logic_trees_forced_numvariables_no_repetation(num_logics, num_variables, depth, allow_True_False):
    logics = set()
    while len(logics) < num_logics:
        logic = generate_one_logic(num_variables, depth, allow_True_False)
        tree = Logic(logic)
        if len(tree.leaves) == num_variables:
            logics.add(tree)
    return list(logics)


"""
The following function(s) should not be deprecated.
"""


"""
This function organizes the above functions.
"""
def generate_logic_trees(num_logics, num_variables, depth, disallow_repetetion = True, allow_True_False = False):
    if disallow_repetetion:
        return generate_random_logic_trees_forced_numvariables_no_repetation(num_logics, num_variables, depth, allow_True_False)
    else:
        return generate_random_logic_trees_forced_numvariables(num_logics, num_variables, depth, allow_True_False)