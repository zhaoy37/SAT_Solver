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
        self.pure_positives, self.pure_negatives = self.__find_pure_literals()


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
    This member function finds the literals of self.
    
    Please note that this algorithm by itself can be time-consuming. If interested,
    users can try to isolate this member function for the assignment heuristic mode vs. 
    the mode without assignment heuristic. This may result in different performance
    of the dpll tree under different modes. In our algorithm, this function is called whenever the tree is constructed, 
    and we assume a relatively negligible tree construction time as opposed to formula solving time.
    Other users interested in this are encouraged to separate this member function for different solving modes.
    """
    def __find_pure_literals(self):
        parents = dict()
        for leaf in self.leaves:
            parents[leaf] = []
        # Find the parents of the leaves.
        self.__find_parents_kernel(parents)
        # Find the pure positive and negative literals.
        pure_positives = [leaf for leaf in self.leaves if "not" not in parents[leaf]]
        pure_negatives = [leaf for leaf in self.leaves if (("not" in parents[leaf]) and len(parents[leaf]) == 1)]
        return pure_positives, pure_negatives

    """
    This member function is used in find_pure_literals.
    It finds the parents of the leaves.
    """
    def __find_parents_kernel(self, parents):
        if self.left is not None:
            if self.left.value in self.leaves:
                parents[self.left.value].append(self.value)
            self.left.__find_parents_kernel(parents)
        if self.right is not None:
            if self.right.value in self.leaves:
                parents[self.right.value].append(self.value)
            self.right.__find_parents_kernel(parents)

    """
    Convert parsed logic to a tree recursively.
    """
    def __convert_formula_to_tree(self):
        if not isinstance(self.formula, list):
            return self.formula
        else:
            if self.formula[0] == "not":
                # Perform De Morgan's expansion to work with the pure literals assignment heuristic.
                if isinstance(self.formula[1], list) and self.formula[1][0] == "and":
                    self.left = Logic(["not", self.formula[1][1]])
                    self.right = Logic(["not", self.formula[1][2]])
                    return "or"
                elif isinstance(self.formula[1], list) and self.formula[1][0] == "or":
                    self.left = Logic(["not", self.formula[1][1]])
                    self.right = Logic(["not", self.formula[1][2]])
                    return "and"
                # Perform simplification for double negation so that the tree works with the pure literals assignment heuristic.
                elif isinstance(self.formula[1], list) and self.formula[1][0] == "not":
                    equivalence = Logic(self.formula[1][1])
                    self.left = equivalence.left
                    self.right = equivalence.right
                    return equivalence.value
                else:
                    self.right = Logic(self.formula[1])
                    return self.formula[0]
            else:
                self.left = Logic(self.formula[1])
                self.right = Logic(self.formula[2])
                return self.formula[0]

    """
    This function finds the number of nodes of the tree.
    """
    def num_of_nodes(self):
        if self.left is None and self.right is None:
            return 1
        else:
            if self.left is None:
                return 1 + self.right.num_of_nodes()
            elif self.right is None:
                return 1 + self.left.num_of_nodes()
            else:
                return 1 + self.left.num_of_nodes() + self.right.num_of_nodes()

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
                if tree.value == "and":
                    """
                    Deducing:
                    p | (p or q) and (not p or s)
                    -----------------------------
                    p, s | (p or q) and (not p or s)
                    
                    This is shown to actually slow down the solver. I will figure
                    out how to better integrate this latter (maybe in the solver itself).
                    """
                    # if tree.left.value == "or" and tree.right.value == "or":
                    #     if tree.right.left.value == "not":
                    #         p1 = self.__evaluate_assignment_kernel(assignment, tree.left.left,
                    #                                                tree_heuristic_enabled)
                    #         p2 = self.__evaluate_assignment_kernel(assignment, tree.right.left.right,
                    #                                                tree_heuristic_enabled)
                    #         if p1 and p2:
                    #             return self.__evaluate_assignment_kernel(assignment, tree.right.right,
                    #                                                      tree_heuristic_enabled)

                    """
                    Early termination (case 1):
                    ~p | p and q
                    FALSE | p and q
                    """
                    p = self.__evaluate_assignment_kernel(assignment, tree.left, tree_heuristic_enabled)
                    if not p:
                        return False
                    else:
                        return self.__evaluate_assignment_kernel(assignment, tree.right, tree_heuristic_enabled)

                if tree.value == "or":
                    """
                    Early termination (case 1):
                    p | p or q
                    TRUE | p or q
                    """
                    p = self.__evaluate_assignment_kernel(assignment, tree.left, tree_heuristic_enabled)
                    if p:
                        return True
                    else:
                        return self.__evaluate_assignment_kernel(assignment, tree.right, tree_heuristic_enabled)

            # Naive solution:
            if tree.value == "not":
                return (not self.__evaluate_assignment_kernel(assignment, tree.right, tree_heuristic_enabled))
            elif tree.value == "and":
                return (self.__evaluate_assignment_kernel(assignment, tree.left, tree_heuristic_enabled) and
                        self.__evaluate_assignment_kernel(assignment, tree.right, tree_heuristic_enabled))
            else:
                return (self.__evaluate_assignment_kernel(assignment, tree.left, tree_heuristic_enabled) or
                        self.__evaluate_assignment_kernel(assignment, tree.right, tree_heuristic_enabled))