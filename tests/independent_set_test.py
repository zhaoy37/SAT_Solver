"""
Author: Yiqi (Nick) Zhao

This file tests the independent set solver.

# I used the tutorial here: https://github.com/cgoldberg/python-unittest-tutorial
"""

from problems.independent_set.independent_set_solver import solve_independent_set, find_maximum_independent_set

import unittest

graph = {
    "y1": ["y2", "y3"],
    "y2": ["y4"],
    "y4": ["y5"],
    "y3": ["y1"],
    "y5": ["y4"]
}

# The graph looks like this:
"""
y1 ---- y2----y4----y5
|-------y3
"""

class IndependentSetTest(unittest.TestCase):

    """
    Users are encouraged to try out these tests and customize their own tests
    to gain familiarity with the software.
    """

    def test_graph_Except_0(self):
        self.assertRaises(Exception, solve_independent_set, graph, 0)

    def test_graph_SAT_1(self):
        solution = solve_independent_set(graph, 1)
        self.assertTrue(len(solution) == 1)

    def test_graph_SAT_2(self):
        solution = solve_independent_set(graph, 2)
        self.assertTrue(len(solution) == 2)
        self.assertTrue(solution[1] not in graph[solution[0]])
        self.assertTrue(solution[0] not in graph[solution[1]])

    def test_graph_max(self):
        solution = find_maximum_independent_set(graph)
        self.assertTrue(len(solution) == 3)
        self.assertTrue(solution[0] not in graph[solution[1]])
        self.assertTrue(solution[0] not in graph[solution[2]])
        self.assertTrue(solution[1] not in graph[solution[0]])
        self.assertTrue(solution[1] not in graph[solution[2]])
        self.assertTrue(solution[2] not in graph[solution[0]])
        self.assertTrue(solution[2] not in graph[solution[1]])


    def test_graph_UNSAT(self):
        solution = solve_independent_set(graph, 5)
        self.assertTrue(solution == "UNSAT")

    def test_empty_graph(self):
        self.assertRaises(Exception, solve_independent_set, {}, 3)
        self.assertRaises(Exception, find_maximum_independent_set, {})

    def test_graph_with_one_node(self):
        solution = solve_independent_set({"y0": []}, 1)
        self.assertTrue(len(solution) == 1)
        self.assertTrue(solution[0] == "y0")
        solution = find_maximum_independent_set({"y0": []})
        self.assertTrue(len(solution) == 1)
        self.assertTrue(solution[0] == "y0")


if __name__ == '__main__':
    unittest.main()