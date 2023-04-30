"""
Author: Ziyan An
Reference: https://docs.python.org/3/library/unittest.html 

Implementation for tests on OBDD.
"""

import os
import sys
sys.path.append('../')
import unittest
from shared.logic_parser import parse_logic
from bdd.robdd_graph import ROBDD_graph
from bdd.robdd_solver import convert_robdd_graph, construct_obdd, robddPaths, allPaths


def compare_bdd(node1=None, node2=None):
    """
    Compares if two OBDDs evaluate to the same result.
    """
    path_1 = list(allPaths(node1))
    path_2 = list(allPaths(node2))
    cleaned_1 = [sorted(p[0]) for p in path_1]
    cleaned_2 = [sorted(p[0]) for p in path_2]
    for p in cleaned_1:
        if not p in cleaned_2:
            return False
    return True



class OBDDTestMethods(unittest.TestCase):
    
    def test_obdd_single_short(self):
        formula = "((x0 or (not x1)) and (x1 or x2))" 
        logic = parse_logic(formula)
        ordering = [2, 1, 0]
        obdd = construct_obdd(ordering, logic, vis=False)

    def test_obdd_single_long(self):
        formula = "(((not x0) and (not x1) and (not x2)) or (x0 and x1) or (x1 and x2))"
        logic = parse_logic(formula)
        ordering = [2, 1, 0]
        obdd = construct_obdd(ordering, logic, vis=False)

    def test_obdd_changed_order(self):
        formula = "((x0 or (not x1)) and (x1 or x2))" 
        logic = parse_logic(formula)
        ordering = [0, 1, 2]
        obdd_1 = construct_obdd(ordering, logic, vis=False)
        logic = parse_logic(formula)
        ordering = [2, 1, 0]
        obdd_2 = construct_obdd(ordering, logic, vis=False)
        self.assertTrue(compare_bdd(obdd_1, obdd_2))

    def test_obdd_long_changed_order(self):
        formula = "(((not x0) and (not x1) and (not x2)) or (x0 and x1) or (x1 and x2))" 
        logic = parse_logic(formula)
        ordering = [0, 1, 2]
        obdd_1 = construct_obdd(ordering, logic, vis=False)
        logic = parse_logic(formula)
        ordering = [2, 1, 0]
        obdd_2 = construct_obdd(ordering, logic, vis=False)
        self.assertTrue(compare_bdd(obdd_1, obdd_2))

    def test_obdd_correst(self):
        formula = "((x0 or (not x1)) and (x1 or x2))" 
        logic = parse_logic(formula)
        ordering = [0, 1, 2]
        obdd_1 = construct_obdd(ordering, logic, vis=False)
        path_1 = list(allPaths(obdd_1))
        cleaned_1 = [sorted(p[0]) for p in path_1]
        [[(-1, 0), (0, 0), (1, 0), (2, 0)], 
         [(-1, 1), (0, 0), (1, 0), (2, 1)], 
         [(-1, 0), (0, 0), (1, 1), (2, 0)], 
         [(-1, 0), (0, 0), (1, 1), (2, 1)], 
         [(-1, 0), (0, 1), (1, 0), (2, 0)], 
         [(-1, 1), (0, 1), (1, 0), (2, 1)], 
         [(-1, 1), (0, 1), (1, 1), (2, 0)], 
         [(-1, 1), (0, 1), (1, 1), (2, 1)]] 


if __name__ == '__main__':
    unittest.main()