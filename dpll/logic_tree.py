"""
Author: Yiqi (Nick) Zhao
The purpose of this file is to write the class
for the tree structure of logic formulae.
Acknowledgement: The course materials from
CS 6315 provided by Professor Taylor Johnson are used
for reference purposes.
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
        leaves = [leaf for leaf in leaves if (leaf != "True" and leaf != "False")]
        return set(leaves)


    """
    This method evaluates an assignment.
    The assignment is in the form of a dictionary mapping variables to boolean values.
    """
    def evaluate(self, assignment, tree_heuristics_enabled = True):
        # Check if the assignment dictionary contains and only contains the leaves (excluding true and false) as the keys.
        if self.leaves != set(assignment.keys()):
            raise Exception("The given assignment is not valid")
        return self.__evaluate_assignment_kernel(assignment, self, tree_heuristics_enabled)

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

    """
    This method is the kernel to evaluate a potential assignment.
    The assignment is in the form of a dictionary mapping variables to boolean values.
    """
    def __evaluate_assignment_kernel(self, assignment, tree, tree_heuristic_enabled):
        if (tree.left is None) and (tree.right is None):
            if tree.value == "True":
                return True
            elif tree.value == "False":
                return False
            return assignment[tree.value]
        else:
            # I may allow caching later.
            # Enforce some DPLL heuristics:
            if tree_heuristic_enabled:
                """
                Deducing:
                
                p | (p or q) and (not p or s)
                -----------------------------
                p, s | (p or q) and (not p or s)
                """
                if tree.value == "and":
                    if tree.left.value == "or" and tree.right.value == "or":
                        if tree.right.left.value == "not":
                            p1 = self.__evaluate_assignment_kernel(assignment, tree.left.left,
                                                                   tree_heuristic_enabled)
                            p2 = self.__evaluate_assignment_kernel(assignment, tree.right.left.right,
                                                                   tree_heuristic_enabled)
                            if p1 and p2:
                                return self.__evaluate_assignment_kernel(assignment, tree.right.right,
                                                                         tree_heuristic_enabled)

            # Naive solution:
            if tree.value == "not":
                return (not self.__evaluate_assignment_kernel(assignment, tree.right, tree_heuristic_enabled))
            elif tree.value == "and":
                return (self.__evaluate_assignment_kernel(assignment, tree.left, tree_heuristic_enabled) and
                        self.__evaluate_assignment_kernel(assignment, tree.right, tree_heuristic_enabled))
            else:
                return (self.__evaluate_assignment_kernel(assignment, tree.left, tree_heuristic_enabled) or
                        self.__evaluate_assignment_kernel(assignment, tree.right, tree_heuristic_enabled))