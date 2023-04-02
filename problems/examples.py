"""
Name: Yiqi (Nick) Zhao

This file gives the users some examples for using our created SMT solver to solve some NP-complete problems.
"""

"""
Import the solvers we created.
"""
from graph_coloring.graph_coloring_solver import solve_graph_coloring
from n_queens.n_queens_solver import solve_n_queens


def main():
    """
    Problem 1: Graph coloring.
    """
    # Construct a graph.
    # If you want to use our solver, please enter your graph in adjacency list like the example below.

    # Let the graph be:
    graph = {
        "y1" : ["y2", "y3", "y4"],
        "y2": ["y3"],
        "y3": [],
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
    print("Solving the N-Queens problem: Example 1 (N = 3) --> Expected: UNSAT")
    print("Solution from the solver:")
    print(solve_n_queens(3))
    print()
    print("Solving the N-Queens problem: Example 2 (N = 4) --> Expected: This should be solvable.")
    print("Solution from the solver:")
    print(solve_n_queens(4))
    print()
    print("Solving the N-Queens problem: Example 2 (N = 8) --> Expected: This should be solvable. It may take a while.")
    print("Solution from the solver:")
    print(solve_n_queens(8))
    print()



if __name__ == "__main__":
    main()