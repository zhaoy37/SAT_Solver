"""
Author: Yiqi (Nick) Zhao

This file tests the Partition Problem Solver.

# I used the tutorial here: https://github.com/cgoldberg/python-unittest-tutorial
"""

from problems.partition.partition_solver import solve_partition

import unittest

class PartitionTest(unittest.TestCase):

    """
    Users are encouraged to try out these tests and customize their own tests
    to gain familiarity with the software.
    """

    def test_case_length_0(self):
        solution = solve_partition([])
        self.assertTrue(solution == "UNSAT")

    def test_case_length_1(self):
        solution = solve_partition([1])
        self.assertTrue(solution == "UNSAT")

    def test_case_length_2_SAT(self):
        part1, part2 = solve_partition([1, 1])
        self.assertTrue(sum(part1) == sum(part2))

    def test_case_length_2_UNSAT(self):
        solution = solve_partition([3, 4])
        self.assertTrue(solution == "UNSAT")

    def test_case_length_3_SAT(self):
        part1, part2 = solve_partition([1, 0, 1])
        self.assertTrue(sum(part1) == sum(part2))


if __name__ == '__main__':
    unittest.main()