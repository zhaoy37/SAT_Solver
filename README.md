# Boolean Satisfiability (SAT) Solver: Applications and Theory

## Introduction
This project is the course final project from CS 6315 (Automated Verification) at Vanderbilt University. The project authors are **Yiqi (Nick) Zhao** and **Ziyan An**, with the help from the instructor, **Professor Taylor Johnson**. In this project, we create solvers for *Boolean Satisfiability Problems* (SAT Problems) using both the *Davis-Putnam-Logemann-Loveland (DPLL) algorithm* and *Reduced-order binary decision diagrams (ROBDDs)*. Then, we create a *Satisfiability Modulo Theories* (SMT) solver for predicates over integers using our created SAT solver. We further apply this SMT solver to create solvers for a variety of interesting problems (which can be reduced to solving SMT problems). For more information on some details of our project, feel free to read our report, attached to this github repository (**to be done later**).

The purpose of the project is to allow interested readers to learn some classical SAT solving techniques and how they can be applied to solve other classical problems in algorithms through reading this user mannual and the actual codes. **The project is educational in nature and is not necessarily the state-of-the-art.** If you want a faster SAT/SMT solver, please refer to other softwares such as Z3. For the rest of this mannual, we will discuss how users can use our project in detail following a **top-down approach**, with a discussion on solving problems in algorithms using an SMT solver followed by a detailed introduction to the SMT and SAT solving strategies.

To run the solver, please clone the github repository and run the command `python3 main.py`, which directs you to using the SAT solvers.

## Applications
### Background knowledge on SAT and SMT
Imagine that you are provided with a boolean formula P and asked to determine if P is *satisfiable*. P is satisfiabile if there exists values for each variable such that P evaluates to true. For example, the formula $P = (x1 \wedge x2) \vee x3$ is satisfiable because there exists a model {x1 = 1, x2 = 1, x3 = 0} such that the the boolean formula evaluates to true. On the contrary, $P = (x1 \wedge \neg x1)$ is not satisfiable. *Validity* means that the formula evaluates to true for all models.

The implication of SAT solving is theoretically supported by the *Cook-Levin Theorem*, which states that Boolean SAT is NP-complete. Equivalently, any problem in NP can be reduced in polynomial time by a deterministic Turing Machine to a SAT problem. Therefore, many classical NP-complete problems in algorithms, such as graph coloring and sudoku, can be encoded into a SAT Problem representation and solved via a SAT solver. However, for abstraction purposes, such problems can be better represented using SMT.

The SMT problem is similar to the SAT Problem with the exception that the formulas are many-sorted. In our project, we only consider the SMT problem over integer predicates with no support for arithmetic operators that are not in the set of ${=, \le, \ge}$, because this representation scheme is all we need to solve the problems in the /problems folder. However, such scheme can be easily expanded to a broader set of operators and predicate domains.

For more details on how to use the SMT solver we created, including how to provide SMT encodings to the solver, please refer to the Theory section. In a nutshell, in our SMT solver, we encode SMT problems as SAT problem representation with each SAT variable represents one SMT clause, and we solve the corresponding SAT problem and use recursive backtracking to find the SMT assignments that fits a solution to the SAT problem.

We will proceed to introduce some interesting problems we solve using our created SMT solver. To see the codes on solving the problems, please refer to the /problems sub-directory and the example.py file inside the sub-directory.

### Graph Coloring
Graph coloring is an NP-complete problem. Specifically, we focus on vertex-coloring: Given a graph and a number of colors allowed, assign each node in the graph a color such that there does not exist a pair of adjacent nodes with the same color.

To use our solver, call the `solve_graph_coloring` function from /`problems/graph_coloring/graph_coloring_solver`. The two arguments are `graph`, which is an adjacency list representation of a graph, and `num_colors`, which denotes the **maximum number** allowed to color the graph. The function returns the assignment of chromatic numbers to each node if the problem is solvable (if the node does not appear in the assignment, it can be any color within the set of all chromatic numbers). In the case of an unsolvable problem, the solver returns "UNSAT". 


Internally, the solver constructs the SMT encoding in the following way: 1) Each SMT clause dictates that the chromatic number of a node cannot be equal to that of one of its adjacent node. 2) Form the SAT representation of the SMT clauses by taking conjunctions of the SMT clauses, which cover all possible edges of the graph. 3)Use the SMT solver to solve the encoded SMT problem.

## Acknowledgements
Throughout the tutorial and the codes for this project, we borrowed some materials from the lecture slides provided by Professor Taylor Johnson from CS 6315.
