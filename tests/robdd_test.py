"""
Author: Ziyan An
Reference: https://docs.python.org/3/library/unittest.html 

Implementation for tests on ROBDD.
"""

import unittest
from shared.logic_parser import parse_logic
from bdd.robdd_graph import ROBDD_graph
from bdd.robdd_solver import convert_robdd_graph, construct_obdd, robddPaths