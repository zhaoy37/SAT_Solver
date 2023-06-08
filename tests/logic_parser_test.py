"""
Author: Yiqi (Nick) Zhao

This file tests the logic parser.

# I used the tutorial here: https://github.com/cgoldberg/python-unittest-tutorial
"""

from resources.logic_parser import parse_logic

import unittest

class ParserTest(unittest.TestCase):

    """
    Users are encouraged to try out these tests and customize their own tests
    to gain familiarity with the software.
    """

    def test_case_1(self):
        parsed = parse_logic("x1 and x2")
        self.assertListEqual(parsed, ["and", "x1", "x2"])

    def test_case_2(self):
        parsed = parse_logic("x1 and x2 or not x3")
        self.assertListEqual(parsed, ["or", ["and", "x1", "x2"], ["not", "x3"]])

    def test_case_3(self):
        parsed = parse_logic("x1 and x2 or x3 and not x4")
        self.assertListEqual(parsed, ["or", ["and", "x1", "x2"], ["and", "x3", ["not", "x4"]]])


if __name__ == '__main__':
    unittest.main()