"""
Name: Yiqi (Nick) Zhao

This file gives the users some examples for using our created SMT solver to solve some NP-complete problems.
"""

"""
Import the solvers we created.
"""
from graph_coloring.graph_coloring_solver import solve_graph_coloring
from n_queens.n_queens_solver import solve_n_queens
from subset_sum.subset_sum_solver import solve_subset_sum
from independent_set.independent_set_solver import solve_independent_set, find_maximum_independent_set
from partition.partition_solver import solve_partition


def main(method='dpll'):
    """
    Problem 1: Graph coloring.
    """
    print("----------Problem 1----------")
    # Construct a graph.
    # If you want to use our solver, please enter your graph in adjacency list like the example below.

    # Let the graph be:
    graph = {
        "y1" : ["y2", "y3", "y4"],
        "y2": ["y3"],
        "y3": ["y2"],
        "y4": []
    }

    # There needs to be at least one connection.

    # This graph is:
    #        y1
    #       / | \
    #      y2 y4 |
    #      |     |
    #      ------y3

    # Now, solve the problem with our solver.

    # First, solve the problem with only 2 colors. This should return UNSAT:
    print("Solving Graph Coloring Problem: Example 1 --> Expected: UNSAT")
    print("Solution from our solver:", solve_graph_coloring(graph, 2))
    print()

    # Now, solve the problem with 3 colors. This is solvable.
    print("Solving Graph Coloring Problem: Example 2 --> Expected: This should be solvable.")
    print("Solution from our solver:", solve_graph_coloring(graph, 3))
    print()

    """
    Problem 2: N-Queens
    """
    print("----------Problem 2----------")
    print("Solving the N-Queens problem: Example 1 (N = 3) --> Expected: UNSAT")
    print("Solution from the solver:")
    print(solve_n_queens(3, method = "minconflicts"))
    print()
    print("Solving the N-Queens problem: Example 2 (N = 4) --> Expected: This should be solvable.")
    print("Solution from the solver:")
    print(solve_n_queens(4, method = "minconflicts"))
    print()
    print("Solving the N-Queens problem: Example 2 (N = 8) --> Expected: This should be solvable. It may take a while.")
    print("Solution from the solver:")
    print(solve_n_queens(8, method = "minconflicts"))
    print()

    """
    Problem 3: Subset Sum
    """
    print("----------Problem 3----------")
    print("Solving the subset sum problem: [1, 2] -> 1 --> Expected: SAT")
    print(solve_subset_sum([1, 2], 1))
    print()
    print("Solving the subset sum problem: [1, 2] -> 3 --> Expected: SAT")
    print(solve_subset_sum([1, 2], 3))
    print()
    print("Solving the subset sum problem: [1, 2] -> 4 --> Expected: UNSAT")
    print(solve_subset_sum([1, 2], 4))
    print()

    """
    Problem 4: Independent Set
    """
    print("----------Problem 4----------")
    print("Solving independent set problem with cardinality 1 on the same graph for Problem 1. --> Expected: SAT")
    print(solve_independent_set(graph, 1))
    print("Solving independent set problem with cardinality 3 on the same graph for Problem 1. --> Expected: UNSAT")
    print(solve_independent_set(graph, 3))
    print("Finding the maximum independent set --> Expected: SAT")
    print(find_maximum_independent_set(graph))
    print()

    """
    Problem 5: Partition
    """
    print("----------Problem 5----------")
    print("Solving the Partition Problem: [1, 5, 4] --> Expected: SAT")
    print(solve_partition([1, 5, 4]))
    print("Solving the Partition Problem: [3, 3] --> Expected: SAT")
    print(solve_partition([3, 3]))
    print("Solving the Partition Problem: [1, 2] --> Expected: UNSAT")
    print(solve_partition([1, 2]))


if __name__ == "__main__":
    main()