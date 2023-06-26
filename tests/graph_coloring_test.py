"""
Author: Yiqi (Nick) Zhao

This file tests the graph coloring.

# I used the tutorial here: https://github.com/cgoldberg/python-unittest-tutorial
"""

from problems.graph_coloring.graph_coloring_solver import solve_graph_coloring

import unittest

graph = {
    "y1": ["y2", "y3"],
    "y2": ["y4"],
    "y4": ["y5"],
    "y5": ["y4"],
    "y3": ["y1"]
}

# The graph looks like this:
"""
y1 ---- y2----y4----y5
|-------y3
"""

class GraphColoringTest(unittest.TestCase):

    """
    Users are encouraged to try out these tests and customize their own tests
    to gain familiarity with the software.
    """

    def test_graph_SAT(self):
        solution = solve_graph_coloring(graph, 2)
        y1 = solution["y1"]
        y2 = solution["y2"]
        y3 = solution["y3"]
        y4 = solution["y4"]
        y5 = solution["y5"]
        self.assertTrue(y1 != y2)
        self.assertTrue(y2 != y4)
        self.assertTrue(y1 != y3)
        self.assertTrue(y4 != y5)

    def test_graph_UNSAT(self):
        solution = solve_graph_coloring(graph, 1)
        self.assertTrue(solution == "UNSAT")

    # Test two directions.
    def test_graph_SAT_2(self):
        solution = solve_graph_coloring(graph, 3)
        y1 = solution["y1"]
        y2 = solution["y2"]
        y3 = solution["y3"]
        y4 = solution["y4"]
        y5 = solution["y5"]
        self.assertTrue(y1 != y2)
        self.assertTrue(y2 != y4)
        self.assertTrue(y1 != y3)
        self.assertTrue(y4 != y5)

    def test_exception_1(self):
        self.assertRaises(Exception, solve_graph_coloring, graph, 10)

    def test_exception_2(self):
        self.assertRaises(Exception, solve_graph_coloring, {"y1" : []}, 1)


if __name__ == '__main__':
    unittest.main()