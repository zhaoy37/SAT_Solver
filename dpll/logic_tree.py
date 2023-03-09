"""
Author: Nick

The purpose of this file is to write the class
for the tree structure of logic formulae.
"""

class Logic:

    """
    Constructor
    """
    def __init__(self, formula):
        self.formula = formula
        self.left = None
        self.right = None
        self.value = self.__convert_formula_to_tree()
        self.leaves = self.load_leaves()

    """
    Perform an in-oder traversal of the tree for printing.
    This member function is majorly constructed for testing purposes.
    """
    def print_tree(self):
        if self.left is not None:
            self.left.print_tree()
        print(self.value)
        if self.right is not None:
            self.right.print_tree()

    """
    This member function finds the leaves of self.
    """
    def load_leaves(self):
        # Perform an in-order traversal.
        leaves = []
        if self.left is not None:
            leaves.extend(self.left.load_leaves())
        if (self.left is None) and (self.right is None):
            leaves.append(self.value)
        if self.right is not None:
            leaves.extend(self.right.load_leaves())
        return set(leaves)

    """
    Private methods start here:
    """

    """
    Convert parsed logic to a tree recursively.
    """
    def __convert_formula_to_tree(self):
        if not isinstance(self.formula, list):
            return self.formula
        else:
            if self.formula[0] == "not":
                self.right = Logic(self.formula[1])
                return self.formula[0]
            else:
                self.left = Logic(self.formula[1])
                self.right = Logic(self.formula[2])
                return self.formula[0]