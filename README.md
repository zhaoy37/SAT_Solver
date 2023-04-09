# Boolean Satisfiability (SAT) Solver: Applications and Theory

## Introduction
This project is the course final project from CS 6315 (Automated Verification) at Vanderbilt University. The project authors are **Yiqi (Nick) Zhao** and **Ziyan An**, with the help from the instructor, **Professor Taylor Johnson**. In this project, we create solvers for *Boolean Satisfiability Problems* (SAT Problems) using both the *Davis-Putnam-Logemann-Loveland (DPLL) algorithm* and *Reduced-order binary decision diagrams (ROBDDs)*. Then, we create a *Satisfiability Modulo Theories* (SMT) solver for predicates over integers using our created SAT solver. We further apply this SMT solver to create solvers for a variety of interesting problems (which can be reduced to solving SMT problems). For more information on some details of our project, such as the evaluation, feel free to read our report, attached to this github repository (**to be done later**).

The purpose of the project is to allow interested readers to learn some classical SAT solving techniques and how they can be applied to solve other classical problems in algorithms through reading this user mannual and the actual codes. **The project is educational in nature and is not necessarily the state-of-the-art.** If you want a faster SAT/SMT solver, please refer to other softwares such as Z3. For the rest of this mannual, we will discuss how users can use our project in detail following a **top-down approach**, with a discussion on solving problems in algorithms using an SMT solver followed by a detailed introduction to the SMT and SAT solving strategies.

To run the solver, please clone the github repository and run the command `python3 main.py`, which directs you to using the SAT solvers.

## Applications
### Background knowledge on SAT and SMT
Imagine that you are provided with a boolean formula P and asked to determine if P is *satisfiable*. P is satisfiabile if there exists values for each variable such that P evaluates to true. For example, the formula $P = (x1 \wedge x2) \vee x3$ is satisfiable because there exists a model {x1 = 1, x2 = 1, x3 = 0} such that the the boolean formula evaluates to true. On the contrary, $P = (x1 \wedge \neg x1)$ is not satisfiable. *Validity* means that the formula evaluates to true for all models.

The implication of SAT solving is theoretically supported by the *Cook-Levin Theorem*, which states that Boolean SAT is NP-complete. Equivalently, any problem in NP can be reduced in polynomial time by a deterministic Turing Machine to a SAT problem. Therefore, many classical NP-complete problems in algorithms, such as graph coloring and sudoku, can be encoded into a SAT Problem representation and solved via a SAT solver. However, for abstraction purposes, such problems can be better represented using SMT.

The SMT problem is similar to the SAT Problem with the exception that the formulas are many-sorted. In our project, we only consider the SMT problem over integer predicates with no support for arithmetic operators that are not in the set of ${=, \le, \ge, \lt, \gt, \neq}$, because this representation scheme is all we need to solve the problems in the /problems folder. However, such scheme can be easily expanded to a broader set of operators and predicate domains.

For more details on how to use the SMT solver we creat, including how to provide SMT encodings to the solver, please refer to the Theory section. In a nutshell, in our SMT solver, we encode SMT problems as SAT problem representation with each SAT variable represents one SMT clause, and we solve the corresponding SAT problem and use recursive backtracking to find the SMT assignments that fits a solution to the SAT problem.

We will proceed to introduce some interesting problems we solve using our created SMT solver. To see the codes on solving the problems, please refer to the /problems sub-directory and the example.py file inside the sub-directory.

### Graph Coloring
Graph coloring is an NP-complete problem. Specifically, we focus on vertex-coloring: Given an undirected graph and a number of colors allowed, assign each node in the graph a color such that there does not exist a pair of adjacent nodes with the same color.

To use our solver, call the `solve_graph_coloring` function from `/problems/graph_coloring/graph_coloring_solver.py`. The two arguments are `graph`, which is an adjacency list representation of a graph, and `num_colors`, which denotes the **maximum number** of colors allowed to color the graph. The function returns the assignment of chromatic numbers to each node if the problem is solvable (if the node does not appear in the assignment, it can be any color within the set of all chromatic numbers). In the case of an unsolvable problem, the solver returns "UNSAT". 


Internally, the solver constructs the SMT encoding in the following way: 1) Each SMT clause dictates that the chromatic number of a node cannot be equal to that of one of its adjacent node. 2) Form the SAT representation of the SMT clauses by taking conjunctions of the SMT clauses, which cover all possible edges of the graph. 3)Use the SMT solver to solve the encoded SMT problem.

### N-Queens Problem
In the N-queens problem, given an n by n sized chess board, the algorithm is asked to place n queens on the baord such that no two queen attack each other. 

To use our solver, call the `solve_n_queens` function from `/problems/n_queens/n_queens_solver.py`. The parameter is `num_queens`, which represents the number of queens to be palced (which is equivalent to the length of a side of the square chess board). The function, if the problem is solvable, will return a matrix representing the board, where the 1s denote the placement of the queens and 0s denote empty positions. If the given problem is not solvable, the solver will return "UNSAT".

Inside the solver, each SMT variable represents a column, and the assignmnent to that variable represents the row index of the queen in that column. Then, in the SMT encodings, the solver is supported with representations that no two queen can be in the same row and no two queens can be in the same diagonal. The SAT encoding further abstracts the SMT encodings by connecting the SMT encodings with conjunctions. If the problem is solvable, with the solution, the algorithm transforms the solution into a matrix representation of the chess board.

### Subset Sum
Subset Sum, another NP-Complete algorithm, is stated as follows: Given a list, L, of positive integers, find the subset of the list that sum up to a given value, X. Using the SMT solver, we create a solver for Subset Sum (which is very slow from an application perspective but nonetheless is designed for educational purposes).

Please note that **this implementation can be inconclusive** because of the search space of the SMT solver (whose details are discussed in the next section).

To use the solver, call the `solve_subset_sum` function from `/problems/subset_sum/subset_sum_solver.py`. There are two required parameters: 1) `target_list` denotes the list of nonnegative integers, L. 2) `target_sum` denotes the target, X, of the subset to be summed up to. There are two optional parameters. The `lower_bound` and the `upperbound` allow the user to control the scope of the search space for the SMT solver, which increases the possibility of finding the solution but also increases the time complexity as the search space scope increases. When the solver returns "UNSAT", the algorithm reports inconclusiveness. Otherwise, upon a successful completion, the solver returns a dictionary mapping each index of the list L to a number 1 or 0, where 1 represents the presence of the variable given by that index in the solution subset and 0 represents the non-existence.

Internally, the solver encodes each index of the list to a variable, y_i, with potential values in {0, 1}. Then, the SMT_encoding denotes that `sum(y_i * L[i]) == target_sum`. The SAT_encoding connects the SMT representations via conjunctions.


## Theory
### Theory of SMT Solving

**I said that we are using both of our SAT solvers for this. Currently, it only works for DPLL. We need to integrate ROBDD to this later.**

In this section, we discuss the details of our SMT solver. The solver is limited to predicates over integers. The set of operators allowed for each SMT clause include $=, \le, \ge, \lt, \gt, \neq, +, -, *, //$, where // denotes integer division. The solver only provides single solutions (because that are all we need for solving the problems described in Applications). It is relatively simple to extend the solver to provide multiple solutions. Since the focus of this project is SAT rather than SMT, we only encode features we actually need in the SMT solver without making it overcomplicated. Users are encouraged to optimize and further improve our SMT solver (We use recursive backtracking, but DPLL(T) is a faster algorithm for solving SMT problems).

To use our solver, call the function `solve_SMT` from `/SMT_Solver/smt.py`. The function accepts 5 required parameters (emphasized in bold below): 

#### sat_formula: 
The SAT encoding of the SMT clauses follows the following BNF (where r denotes that the followed string is a regular expression):

`<sat_formula> := <atom> | ["and", <sat_formula>, <sat_formula>] | ["or", <sat_formula>, <sat_formula>] | ["not", <sat_formula>]`

`<atom> := r"x[0-9]+" | True | False`

Semantically, each `<atom>` maps to one SMT clause (True and False are not used in sat_formula for SMT encoding but can be used for SAT formula representations in the next subsection in SAT solving).

#### encodings:
The SMT encoding is a dictionary mapping each atom from the SAT encoding to an SMT clause, where each SMT formula permits the following BNF:

`<smt_formula> := [<operator>, <atom1>, <atom2>]`
 
`<operator> := "le" | "ge" | "eq" | "lt" | "gt" | "nq"`

`<atom1> := <var> | <constant>`

`<atom2> := <var> |<constant>`

`<var> := {any string that does not start with 'x'} | <expression>`

`<expression> = "<subvar> <arith> <subvar>"`

`<arith> := {+, -, *, //}`

`<subvar> := {any literal or integer}`

`<constant> := {any integer}`

Semantically, "le" stands for $\le$, "ge" stands for $\ge$, "lt" stands for $\lt$, "gt" stands for $\gt$, "eq" stands for =, and "nq" stands for $\neq$. The SMT formula `[<operator>, <atom1>, <atom2>]` represents `<atom1> <operator> <atom2>`. For example, ["le", "y1", 2] means y1 < 2. Moreover, the expression "<subvar> <arith> <subvar>" can be taken literally. For example, "y1 + y2" is y1 + y2; "y1 + 3" is y1 + 3.

#### smt_vars:
This is the list of all the variables used in the SMT encoding.

#### lowerbound:
The lower bound of `<constant>`used in the SMT encoding. Semantically, this is the upper bound of the search space. If the solution is outside of the search space, we do not guarantee the correctness.

#### upperbound:
The upper bound of `<constant>`used in the SMT encoding. Semantically, this is the lower bound of the search space. If the solution is outside of the search space, we do not guarantee the correctness.


As an example, to solve $(y1 \le 2) \wedge (y2 = 3)$ with the bounds $0 \le y1, y2 \le 10$, call the function like this: `solve_SMT(["and", "x1", "x2"], {"x1": ["le", "y1", 2], "x2": ["eq", "y2", 3]}, ["y1", "y2"], 0, 10)`.

To solve $(y1 - 2 = y2) \wedge (y2 + y1 > 5)$ with the bounds $0, \le y1, y2 \le 10$, call the function like this: `solve_SMT(["and", "x1", "x2"], {"x1": ["eq", "y1 - 2", "y2"], "x2": ["gt", "y2 + y1", 5]}, ["y1", "y2"], 0, 10)`.

Internally, the SMT solver first finds all possible solutions to the SAT encoding. Consider the example execution: `solve_SMT(["and", "x1", ["not", "x2"]], {"x1" : ["le", "y1", 2], "x2" : ["ge", "y2", 1]}, ["y1", "y2"], 0, 10)`. The SMT solver first uses dpll (default) or robdd to solve the SAT problem `["and", "x1", ["not", "x2"]]`. The only possible solution to the SAT encoding is {"x1" : True, "x2": False}.

Then, the algorithm inverts the false SAT_encoding(s). In the aforementioned example execution, the algorithm generates the following mapping: `{"x1": True, "x2": True} -> {"x1" : ["le", "y1", 2], "x2" : ["lt", "y2", 1]}`.

Lastly, the algorithm uses recursive backtracking to search through the search space of possible assignments, the space of the close intervals from the preselected lowerbound to the upperbound for each SMT variable. In the aforementioned example execution, the algorithm will try the sequence of assignnments {"y1" : 0, "y2" : 0}, {"y1" : 0, "y2" : 1} ... until  {"x1": True, "x2": True} is the mapping`{"x1" : ["le", "y1", 2], "x2" : ["lt", "y2", 1]} -> {"x1": True, "x2": True}` is satisfied. The solver concludes unsatisfiability when the search space runs out for all possible solutions to the SAT encoding.

We choose the above method because it is intuitive. Since the SMT solver is not the focus of the project but rather an abstraction of the SAT solver, we do not focus on the optimization of the SMT solver interface. The algorithm we use is widely used for solving Constraint Satisfaction Problems (CSP), which can be alternatively solved with the min-conflicts algorithm or with recursive backtracking that also integrates the heuristics such as least constrained values. One algorithm that solves a broader set of SMT signatures and possibly with a lower time complexity is DPLL(T), which is the SMT variant of DPLL for SAT Problems. Users are encouraged to replace our SMT solver with other alternatives.

One other essential technique is that although operators {+, -, *, //} connect between only two variables, the users can easily modify the representation for more complicated integer formulas by introducing some temporary variables. For instance, if the user wants to find the solution of `y1 + y2 + y3 = 10` with `0 <= y1, y2, y3 <= 10`, they can call: `solve_SMT(["and", "x1", "x2"],{"x1": ["eq", "y1 + y2", "y4"], "x2": ["eq", "y4 + y3", 10]},["y1", "y2", "y3", "y4"], 0, 10)`.

### Theory of SAT Solving: DPLL
In this section, we discuss the theory of DPLL and how to use the DPLL solver we create. The Davis-Putnam-Logemann-Loveland algorithm (DPLL) is a widely used algorithm in SAT solving. Its basic idea is recursive backtracking search of atom values that meet the satisfiability with some special heuristics. For the rest of this section, we describe how we structure our DPLL SAT solver to implement the search algorithm and the special heuristics.

An input formula is in a format of a list (A SAT formula in human language can be parsed via `/shared/logic_parser.py` to the formula in this format). The syntax and semantics of the list representation is identical to the sat formula described in the `sat_formula` part of the previous subsection. The input to the parser is a human-understandable SAT formula with atoms encoded with `r"x[0-9]+"`. To call the DPLL solver, the user can call the `solve` function in `/dpll/solver/`, which takes the parameter of a tree representation of a given SAT formula (please see the next paragraph for detail). To use the DPLL solver, the parameter `heuristic_enabled` should be True. Another parameter, `multiple` is created to allow the user to choose if the solver provides single or multiple solution(s).

Apart from the solver itself, we also offer a kernel for interacting with the solver, which can be called in `main.py`. The DPLL kernel locates in `/dpll/dpll_kernel.py`. To facilitate evaluation purposes, we also offer a generator that generates SAT formulas in tree representations. The generator can be found in `/shared/logic_generator.py`. The user can think of SAT formulas like trees with "and", "or", "not" represent the non-leaf nodes and the atoms represent the leaf nodes (we will actually discuss this detail of the data structure later in this section). To change the probability each type of non-leaf node occurs, the users can set the probabilities at the top of the program file for the logic generator using the hyperparameters `chance_not`, which denotes the probability that a "not" node occurs, `chance_and`, which denotes the probability that an "and" node occurs, and `chance_or`, which denotes the probability that an "or" node occurs. The user can call `generate_logic_trees` to generate random logic trees following a set of parameters: 1) `num_logics` represent the number of logic trees to be generated. 2) `num_variables` represents the cardinality of SAT atoms in the tree. For instance the cardinality of atoms of `x1 and x2 or x1` is 2. 3) `depth` denotes the depth of each generated tree. The depth is positively correlated with the number of nodes of each SAT tree. 4) `disallow_repetition`, which is optional, denotes if the user allows or disallow repetitions of trees generated. 5) `allow_True_False` representes if the user allows or disallows the presence of pure values True and/or False in the leaf level.

Now, we briefly discuss the heuristics used in DPLL before we introduce the solver implementation: There are two parts of the search algorithm in DPLL. In the recursive backtracking search, the algorithm first decides an assignment. Then, it deduces the assignment by substituting the atoms in the SAT formula with the assignment. If the valuation returns False, the algorithm backtracks to try another assignment if such new assignment is possible. If the algorithm runs out of assignments, the algorithm returns UNSAT. The heuristics in DPLL revolve around heuristics in deciding and deducing.

One heuristic in assigning is *Early termination*, which refers to terminating the algorithm if any realization of a variable leads to True or False of a SAT formula regardless the choice of any other variables. If the algorithmn returns False in the early termination, faster backtracking is encouraged. If the algorithm returns True in the early termination, on the other hand, faster path to a solution is found. To give a concrete example, `$(A \vee B) \wedge (A \vee \neg C)$` is satisfied by `{A = True}`.

One heuristic for deciding assignments is *Pure literals*, which states that if all occurrences of a symbol in the clause have the same sign accross the clause, we can guess that the symbol is True (if the symbol is positive) or False (if the symbol is negative). This can be done with the assumption that any "not" nodes far away from the leaf nodes are transformed to become the parents of the leaf nodes using the rules of De Morgan's Law and double negations. For instance, in $(A \vee B) \wedge (A \vee \neg C) \ wedge (C \vee \neg B)$, the symbol A is pure and positive. By the heuristic, we should prioritize the decision of setting A to True in the search algorithm.

Another heuristic in assigning is *Unit Clauses*, which states that for any clause left with a single literal, we can simplify the clause by realizing that symbol. More broadly speaking, assignments to variables can lead to simplifications and thus a reduction of search space. For instance, in the case of `{A = False}` with $(A \vee B) \ wedge (A \vee \neg C)$, the clause can be simplified to $(B) \wedge (\neg C)$. With this new clause the search space for B and C is reduced.

The above heuristics are what we implement in the DPLL solver. There are some more advanced heuristics that can increase the efficiency of the solver that we did not implement and are discussed below.

Boolean resolution states that if there exists a disjunction of a clause structure, c, and the negation of the same clause structure in a disjunctive normal form, we can eliminate the $c \vee (\neg c)$ from the clause. We did not implement this because it assumes that the clause is in disjunctive normal form, which is not a general assumption we make about the clauses we accept. Some other methods for increasing the solver efficiency include smart variable assignment ordering, devide and conquer and caching.

With the concepts clarified, we want to introduce how our solver approaches SAT solving in detail from an implementation perspective.

When a list representation of a formula is given to the solver, the solver first converts this formula into a binary tree data structure with leaf nodes representing terminal variables and True or False and non-leaf nodes represent negations, conjunctions, and disjunctions. The purpose of the tree is to facilitate the pure-literals heuristics (We assume that the tree construction time is negligible comparing to the solving time in our evaluations). Specifically, using the rules of double negations and De Morgan's Law, we move the negation nodes further down as parents of leaf nodes. Then, we can determine if a node is pure positive or not and if it is pure negative or not.

In the solver, we 

 		


## Tests
To test out the programs, please run the files in the /tests sub-directory. The users are encouraged to create more tests on their own to facilitate the familiarity with the framework. If you notice any issues when testing, please contact yiqi.zhao@vanderbilt.edu. For details on comparing different solvers and more details on the theories, please refer to the report attached with this repository. **(To be added later)**

## Acknowledgements
Throughout the tutorial and the codes for this project, we used some materials from the lecture slides provided by Professor Taylor Johnson from CS 6315. More acknowledgements are in the comments of the codes.
