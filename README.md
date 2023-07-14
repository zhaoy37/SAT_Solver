# Boolean Satisfiability (SAT) Solver: Applications and Theory

## Introduction
This project is the extended work of the course final project from CS 6315 (Automated Verification) at Vanderbilt University. The project authors are **Yiqi (Nick) Zhao** and **Ziyan An**, with the help from the instructor, **Professor Taylor Johnson** and also from **Professor Meiyi Ma**. In this project, we create solvers for *Boolean Satisfiability Problems* (SAT Problems) using both the *Davis-Putnam-Logemann-Loveland (DPLL) algorithm* and *Reduced-order binary decision diagrams (ROBDDs)*. Then, we create a *Satisfiability Modulo Theories* (SMT) solver for predicates over integers using our created SAT solver. We further apply this SMT solver to create solvers for a variety of interesting problems (which can be reduced to solving SMT problems). For more information on some details of our project, such as the evaluation, feel free to read our report (**which has not been updated for the newest improvements**), attached to this github repository.

The purpose of the project is to allow interested readers to learn some classical SAT solving techniques and how they can be applied to solve other classical problems in algorithms through reading this user mannual and the actual codes. **The project is educational in nature and is not necessarily the state-of-the-art.** If you want a faster SAT/SMT solver, please refer to other softwares such as Z3. For the rest of this mannual, we will discuss how users can use our project in detail following a **top-down approach**, with a discussion on solving problems in algorithms using an SMT solver followed by a detailed introduction to the SMT and SAT solving strategies.

To run the solver, please clone the github repository and run the command `python3 main.py`, which directs you to using the SAT and SMT solvers. The solvers accept different SMT kernels. If the user chooses the minconflicts kernel (or if the default is the minconflicts kernel), the algorithm **may be theoretically inconclusive** (as described in the section on the theory of solving SMT problems).

We also provide an interactive tutorial, through which the user can learn about SAT and SMT solving (as well as solving some NP-complete problems) via a jupyter notebook. The user can access the tutorial at `/EduSAT_Interactive_Tutorial/Tutorial on SAT and SMT Solving.ipynb`.

## Python Package
The user is encouraged to try out our python package if they simply want to use the solvers as tools instead of learning about the details. To use the python package, in your terminal, cd to the subfolder `/python_package`. Then, install the wheel file for the python package with the command `pip install edusat-0.0.1-py3-none-any.whl`. There are three parts to the python package:

### sat_solver.sat_solve.

To use the sat solver, in your python file, use the command `from edusat.sat_solver import sat_solve`. The function takes one required parameter `formula` in natural language. Any SAT atom must start with the letter x. The users can selet the method "dpll" vs. "robdd" and multiple = True or multiple = False to control which SAT solving method they want to use and if they want all the solutions (multiple = True) or just one (multiple = False).

To give a concrete example, the return of `sat_solve("x1 or x2", multiple = True)` can be `[{'x1': 1, 'x2': 0}, {'x1': 1, 'x2': 1}, {'x1': 0, 'x2': 1}]` (you can ignore any LALR table generations).

### smt_solver.smt_solve

To use the smt solver, in your python file, use the command `from edusat.smt_solver import smt_solve`. The function takes three required parameters `formula` in natural language, which denotes the SMT formula (where the atoms must start with y), `lower_bound`, which denotes the lower bound of the search range, and `upper_bound`, which denotes the upper bound of the search range. An optional parameter `method` is given for the users to select which solving method to use: "backtracking", "minconflicts", or "robdd". For any information about the parameters please read the tutorials on SMT solving in the tutorial.

To give a concrete example, `smt_solve("y1 < y2 + 1 and y2 > 3", 0, 10)` can be `{'y2': 4, 'y1': 0}`.

## from problems_solver import *

To use any of the solvers described in Section Applications, you can use the command `from edusat.problems_solver import *`.

For instance calling `solve_n_queens(8, method = "minconflicts")` generates the solution to the 8-queens problem.

## Applications
### Background knowledge on SAT and SMT
Imagine that you are provided with a boolean formula P and asked to determine if P is *satisfiable*. P is satisfiabile if there exists values for each variable such that P evaluates to true. For example, the formula $P = (x1 \wedge x2) \vee x3$ is satisfiable because there exists a model {x1 = 1, x2 = 1, x3 = 0} such that the the boolean formula evaluates to true. On the contrary, $P = (x1 \wedge \neg x1)$ is not satisfiable. *Validity* means that the formula evaluates to true for all models.

The implication of SAT solving is theoretically supported by the *Cook-Levin Theorem*, which states that Boolean SAT is NP-complete. Equivalently, any problem in NP can be reduced in polynomial time by a deterministic Turing Machine to a SAT problem. Therefore, many classical NP-complete problems in algorithms, such as graph coloring and sudoku, can be encoded into a SAT Problem representation and solved via a SAT solver. However, for abstraction purposes, such problems can be better represented using SMT.

The SMT problem is similar to the SAT Problem with the exception that the formulas are many-sorted. In our project, we only consider the SMT problem over integer predicates with no support for arithmetic operators that are not in the set of $\{=, \le, \ge, \lt, \gt, \neq, +, -, *, //\}$, because this representation scheme is all we need to solve the problems in the /problems folder. However, such scheme can be easily expanded to a broader set of operators and predicate domains.

For more details on how to use the SMT solver we create, including how to provide SMT encodings to the solver, please refer to the Theory section. In a nutshell, in our SMT solver, we encode SMT problems as SAT problem representation with each SAT variable represents one SMT clause, and we solve the corresponding SAT problem and use recursive backtracking (or minconflicts) to find the SMT assignments that fits a solution to the SAT problem.

We will proceed to introduce some interesting problems we solve using our created SMT solver. To see the codes on solving the problems, please refer to the /problems sub-directory and the example.py file inside the sub-directory.

### Graph Coloring
Graph coloring is an NP-complete problem. Specifically, we focus on vertex-coloring: Given an undirected graph and a number of colors allowed, assign each node in the graph a color such that there does not exist a pair of adjacent nodes with the same color. The default SMT kernel used for this solver is backtracking.

To use our solver, call the `solve_graph_coloring` function from `/problems/graph_coloring/graph_coloring_solver.py`. The two arguments are `graph`, which is an adjacency list representation of a graph, and `num_colors`, which denotes the **maximum number** of colors allowed to color the graph. The function returns the assignment of chromatic numbers to each node if the problem is solvable (if the node does not appear in the assignment, it can be any color within the set of all chromatic numbers). In the case of an unsolvable problem, the solver returns "UNSAT". 


Internally, the solver constructs the SMT encoding in the following way: 1) Each SMT clause dictates that the chromatic number of a node cannot be equal to that of one of its adjacent node. 2) Form the SAT representation of the SMT clauses by taking conjunctions of the SMT clauses, which cover all possible edges of the graph. 3) Use the SMT solver to solve the encoded SMT problem.

### N-Queens Problem
In the N-queens problem, given an n by n sized chess board, the algorithm is asked to place n queens on the board such that no two queen attack each other. The default SMT kernel used for this problem is backtracking.

To use our solver, call the `solve_n_queens` function from `/problems/n_queens/n_queens_solver.py`. The parameter is `num_queens`, which represents the number of queens to be palced (which is equivalent to the length of a side of the square chess board). The function, if the problem is solvable, will return a matrix representing the board, where the 1s denote the placement of the queens and 0s denote empty positions. If the given problem is not solvable, the solver will return "UNSAT".

Inside the solver, each SMT variable represents a column, and the assignmnent to that variable represents the row index of the queen in that column. Then, in the SMT encodings, the solver is supported with representations that no two queen can be in the same row and no two queens can be in the same diagonal. The SAT encoding further abstracts the SMT encodings by connecting the SMT encodings with conjunctions. If the problem is solvable, with the solution, the algorithm transforms the solution into a matrix representation of the chess board.

### Subset Sum
Subset Sum, another NP-Complete problem, is stated as follows: Given a list, L, of positive integers, find the subset of the list that sum up to a given value, X. Using the SMT solver, we create a solver for Subset Sum. The default SMT kernel for this solver is backtracking.

To use the solver, call the `solve_subset_sum` function from `/problems/subset_sum/subset_sum_solver.py`. There are two required parameters: 1) `target_list` denotes the list of nonnegative integers, L. 2) `target_sum` denotes the target, X, of the subset to be summed up to. There are two optional parameters. When the solver returns "UNSAT", the algorithm reports that the problem is not feasible. Otherwise, upon a successful completion, the solver returns a dictionary mapping each index of the list L to a number 1 or 0, where 1 represents the presence of the variable given by that index in the solution subset and 0 represents the non-existence.

Internally, the solver encodes each index of the list to a variable, y_i, with potential values in {0, 1}. Then, the SMT_encoding denotes that `sum(y_i * L[i]) == target_sum`. The SAT_encoding connects the SMT representations via conjunctions.

### Independent Set
Independent Set is an NP-Complete Problem. We frame our variant of the Independent Set problem below:

Find a set A, a subset of V, in an undirected graph G = (V, E), where every node in A is not adjacent to any other node in A and the cardinality of A is k.

We also frame the maximum independent set problem as the problem to find A with largest possible k.

The default SMT kernel for this solver is backtracking.

To use our solver to solve the independent set problem, call the `solve_independent_set` function from `/problems/independent_set_solver.py`. There are two required parameters: 1) `graph` denotes the adjacency list representation of the undirected graph G. Please refer to `/problems/examples.py` to see an example. 2) `target_cardinality` denotes the cardinality, k, of the independent set, A. If the problem is solvable, the function will return a list of nodes, which is a candidate solution for A. Otherwise, "UNSAT" will be returned.

We also create a solver for the maximum independent set problem: To solve the maximum independent set problem, call the `find_maximum_independent_set` function from `problems/independent_set_solver.py`. The only required parameter is `graph`, which has the same meaning as the graph in the independent set problem solver.

For the independent set problem solver, the algorithm treats each node to take either values of 0 and 1. The constraints are that the sum of the values of two adjacent nodes is less then 2, and the sum of all the nodes in the graph equals the target cardinality. The SMT representation is then solved using our solver for SMT problems. For the maximum independent set problem solver, the algorithm keeps calling the independent set problem solver with incrementally larger value of target cardinality with a incrementation of 1 until "UNSAT" is returned. Then, the algorithm returns the solution with target cardinality one smaller than the cardinality that triggers the infeasibility.

### Partition Problem
The Partition Problem is NP-complete, and is defined below for our solver implementation:

Given a list L, of integers, partition L into two sublists such that the sum of one sublist equals the sum of the other sublist.

We only focus on integer lists because the SMT solver we implement only work for integer predicates. The default SMT kernel for this solver is backtracking.

To use the solver, call the `solve_partition` function from `/problems/partition/partition_solver.py`. There is one required parameter, *target_list*, which is the list, L, to be analyzed. When the solver returns "UNSAT", the algorithm reports infeasibility. Otherwise, upon a successful completion, the solver returns two sublists that form the partition of the target list.

Internally, the solver encodes each index of the list to a variable (y_i) with a potential values in {0, 1}. Then, the SMT_encoding represents `sum(y_i * L[i]) * 2 == sum(L[i])`. Thus, All variables that have the same assigned value form one group. The algorithm treats the two groups as the partition of the target list. In our SMT encoding, we also dictate that the sum of all y_i cannot be 0 or the length of the target list to prevent the case where a group among the two groups is an empty set.

## Theory
### Theory of SMT Solving

In this section, we discuss the details of our SMT solvers. The solvers are limited to predicates over integers. The set of operators allowed for each SMT clause include $=, \le, \ge, \lt, \gt, \neq, +, -, *, //$, where // denotes integer division. The solvers only provide single solutions (because that are all we need for solving the problems described in Applications). It is relatively simple to extend the solvers to provide multiple solutions. Since the focus of this project is SAT rather than SMT, we only encode features we actually need in the SMT solver without making it overcomplicated. Users are encouraged to optimize and further improve our SMT solver.

To use our solver, call the function `solve_SMT` from `/SMT_Solver/smt.py`. Currently, we support three algorithms in the SMT solver, which can be envoked by setting the optional argument `method` in the function:

1. Setting `method` to "backtracking" envokes the naive backtracking approach with a DPLL SAT Solver.

2. Setting `method` to "robdd" envokes the naive backtracking approach with a ROBDD SAT Solver.

3. Setting `method` to "minconflicts" (which is the default) envokes the min-conflicts solver from the common min-conflicts algorithm from the Constraint Satisfaction Problem (CSP). The SAT solving approach is DPLL. Please note that this kernel can result in UNSAT even if there exists a solution if the number of termination steps is not sufficiently large (which may result in inability to find a solution if SAT). However, this kernel can be faster in solving certain problems than the naive backtracking approach if the problem is solvable.

We also offer an interface where the solvers can solve the SMT problems in natural language (standard representations) given by the users. The users can call the solver via `main.py`.

The function `solve_SMT` accepts 5 required parameters (emphasized in bold below): 

#### sat_formula: 
The SAT encoding of the SMT subclauses follows the following BNF (where r denotes that the followed string is a regular expression):

`<sat_formula> := <atom> | ["and", <sat_formula>, <sat_formula>] | ["or", <sat_formula>, <sat_formula>] | ["not", <sat_formula>]`

`<atom> := r"x[0-9]+" | True | False`

Semantically, each `<atom>` maps to one SMT subclause (True and False are not used in sat_formula for SMT encoding but can be used for SAT formula representations in the next subsection in SAT solving).

#### encodings:
The SMT encoding is a dictionary mapping each atom from the SAT encoding to an SMT subclause, where each SMT formula permits the following BNF:

`<smt_formula> := [<operator>, <expression>, <expression>]`
 
`<operator> := "le" | "ge" | "eq" | "lt" | "gt" | "nq"`

`<expression> := {any integer or string with mathematical expressions with allowed operators without using r'x[0-9]*' or r'X[0-9]*'}`

Semantically, "le" stands for $\le$, "ge" stands for $\ge$, "lt" stands for $\lt$, "gt" stands for $\gt$, "eq" stands for =, and "nq" stands for $\neq$. The SMT formula `[<operator>, <expression1>, <expression2>]` represents `<expression1> <operator> <expression2>`. For example, ["lt", "y1", 2] means y1 < 2.

#### smt_vars:
This is the list of all the variables used in the SMT encoding.

#### lowerbound:
Semantically, this is the lower bound of the search space (the lower bound of that any SMT variable can be assigned to). If the solution is outside of the search space, we do not guarantee the correctness.

#### upperbound:
Semantically, this is the upper bound of the search space (the upper bound of that any SMT variable can be assigned to). If the solution is outside of the search space, we do not guarantee the correctness.

As an example, to solve $(y1 \le 2) \wedge (y2 = 3)$ with the bounds $0 \le y1, y2 \le 10$, call the function like this: `solve_SMT(["and", "x1", "x2"], {"x1": ["le", "y1", 2], "x2": ["eq", "y2", 3]}, ["y1", "y2"], 0, 10)`.

To solve $(y1 - 2 = y2) \wedge (y2 + y1 > 5)$ with the bounds $0 \le y1, y2 \le 10$, call the function like this: `solve_SMT(["and", "x1", "x2"], {"x1": ["eq", "y1 - 2", "y2"], "x2": ["gt", "y2 + y1", 5]}, ["y1", "y2"], 0, 10)`.

Internally, the SMT solver first finds all possible solutions to the SAT encoding. Consider the example execution: `solve_SMT(["and", "x1", ["not", "x2"]], {"x1" : ["le", "y1", 2], "x2" : ["ge", "y2", 1]}, ["y1", "y2"], 0, 10)`. The SMT solver first uses dpll (default) or robdd to solve the SAT problem `["and", "x1", ["not", "x2"]]`. The only possible solution to the SAT encoding is {"x1" : True, "x2": False}.

Then, the algorithm inverts the false SAT_encoding(s). In the aforementioned example execution, the algorithm generates the following mapping: `{"x1": True, "x2": True} -> {"x1" : ["le", "y1", 2], "x2" : ["lt", "y2", 1]}`.

Lastly, the algorithm calls on the kernel for SMT solving.

When calling the kernel "robdd" or "backtracking", the solver uses recursive backtracking to search through the search space of possible assignments, the space of the close intervals from the preselected lowerbound to the upperbound for each SMT variable. In the aforementioned example execution, the algorithm will try the sequence of assignnments {"y1" : 0, "y2" : 0}, {"y1" : 0, "y2" : 1} ... until  {"x1": True, "x2": True} is the mapping`{"x1" : ["le", "y1", 2], "x2" : ["lt", "y2", 1]} -> {"x1": True, "x2": True}` is satisfied. The solver concludes unsatisfiability when the search space runs out for all possible solutions to the SAT encoding.

When calling the kernel "minconflicts", the solver uses the min-conflicts algorithm commonly used for solving Constraint Satisfaction Problem. The algorithm first randomly initializes the values (given the bounds) for the set of all SMT variables. While the assignment does not satisfy the formula, the algorithm randomly picks a variable from all the set of SMT variables that result in conflict(s), and find the value that best reduces the conflicts associated with that variable to update the assignment (the value found is equivalent to the value that best reduces the conflicts in the existing state of the assignment). The algorithm terminates when an assignment is found to satisfy the SMT formula or when the maximum number of iteration steps is achieved. Please note that "UNSAT" may be found even if there exists a solution if the maximum iteration steps is not sufficiently large. However, this approach can be faster than the naive backtracking approach when applied to some of our NP-complete problem solver(s) such as the N-queens problem solver.

One algorithm, which we want to focus on in the future, that solves a broader set of SMT signatures and possibly with a lower time complexity is DPLL(T), which is the SMT variant of DPLL for SAT Problems. Users are encouraged to replace our SMT solver with other alternatives.

### Theory of SAT Solving: DPLL
In this section, we discuss the theory of DPLL and how to use the DPLL solver we create. The Davis-Putnam-Logemann-Loveland algorithm (DPLL) is a widely used algorithm in SAT solving. Its basic idea is recursive backtracking search of atom values that meet the satisfiability with some special heuristics. For the rest of this section, we describe how we structure our DPLL SAT solver to implement the search algorithm and the special heuristics.

An input formula is in a format of a list (A SAT formula in human language can be parsed via `/shared/logic_parser.py` to the formula in this format). The syntax and semantics of the list representation is identical to the sat formula described in the `sat_formula` part of the previous subsection. The input to the parser is a human-understandable SAT formula with atoms encoded with `r"x[0-9]+"`. To call the DPLL solver, the user can call the `solve` function in `/dpll/solver/`, which takes the parameter of a tree representation of a given SAT formula (please see the next paragraph for detail). To use the DPLL solver, the parameter `heuristic_enabled` should be True. Another parameter, `multiple` is created to allow the user to choose if the solver provides single or multiple solution(s).

Apart from the solver itself, we also offer a kernel for interacting with the solver, which can be called in `main.py`. The DPLL kernel locates in `/dpll/dpll_kernel.py`. To facilitate evaluation purposes, we also offer a generator that generates SAT formulas in tree representations. The generator can be found in `/shared/logic_generator.py`. The user can think of SAT formulas like trees with "and", "or", "not" represent the non-leaf nodes and the atoms represent the leaf nodes (we will actually discuss this detail of the data structure later in this section). To change the probability each type of non-leaf node occurs, the users can set the probabilities at the top of the program file for the logic generator using the hyperparameters `chance_not`, which denotes the probability that a "not" node occurs, `chance_and`, which denotes the probability that an "and" node occurs, and `chance_or`, which denotes the probability that an "or" node occurs. The user can call `generate_logic_trees` to generate random logic trees following a set of parameters: 1) `num_logics` represent the number of logic trees to be generated. 2) `num_variables` represents the cardinality of SAT atoms in the tree. For instance the cardinality of atoms of `x1 and x2 or x1` is 2. 3) `depth` denotes the depth of each generated tree. The depth is positively correlated with the number of nodes of each SAT tree. 4) `disallow_repetition`, which is optional, denotes if the user allows or disallow repetitions of trees generated. 5) `allow_True_False` representes if the user allows or disallows the presence of pure values True and/or False in the leaf level.

Now, we briefly discuss the heuristics used in DPLL before we introduce the solver implementation: There are two parts of the search algorithm in DPLL. In the recursive backtracking search, the algorithm first decides an assignment. Then, it deduces the assignment by substituting the atoms in the SAT formula with the assignment. If the valuation returns False, the algorithm backtracks to try another assignment if such new assignment is possible. If the algorithm runs out of assignments, the algorithm returns UNSAT. The heuristics in DPLL revolve around heuristics in deciding and deducing.

One heuristic in assigning is *Early termination*, which refers to terminating the algorithm if any realization of a variable leads to True or False of a SAT formula regardless the choice of any other variables. If the algorithmn returns False in the early termination, faster backtracking is encouraged. If the algorithm returns True in the early termination, on the other hand, faster path to a solution is found. To give a concrete example, $(A \vee B) \wedge (A \vee \neg C)$ is satisfied by `{A = True}`.

One heuristic for deciding assignments is *Pure literals*, which states that if all occurrences of a symbol in the clause (assuming a negation normal form) have the same sign accross the clause, we can guess that the symbol is True (if the symbol is positive) or False (if the symbol is negative). This can be done with the assumption that any "not" nodes far away from the leaf nodes are transformed to become the parents of the leaf nodes using the rules of De Morgan's Law and double negations. For instance, in $(A \vee B) \wedge (A \vee \neg C) \wedge (C \vee \neg B)$, the symbol A is pure and positive. By the heuristic, we should prioritize the decision of setting A to True over setting A to False in the search algorithm.

Another heuristic in assigning is *Unit Clauses*, which states that for any clause left with a single literal, we can simplify the clause by realizing that symbol. More broadly speaking, assignments to variables can lead to simplifications. For instance, in the case of `{A = False}` with $(A \vee B) \wedge (A \vee \neg C)$, the clause can be simplified to $(B) \wedge (\neg C)$.

The above heuristics are what we implement in the DPLL solver. There are some more advanced heuristics that can increase the efficiency of the solver that we did not implement and are discussed below.

Boolean resolution states that if there exists a disjunction of a clause structure, c, and the negation of the same clause structure in a disjunctive normal form, we can eliminate the $c \vee (\neg c)$ from the clause. We did not implement this because it assumes that the clause is in disjunctive normal form, which is not a general assumption we make about the clauses we accept. Some other methods for increasing the solver efficiency include smart variable assignment ordering, devide and conquer and caching.

With the concepts clarified, we want to introduce how our solver approaches SAT solving in detail from an implementation perspective.

When a list representation of a formula is given to the solver, the solver first converts this formula into a binary tree data structure with leaf nodes representing terminal variables and True or False and non-leaf nodes represent negations, conjunctions, and disjunctions. The purpose of the tree is to facilitate the pure-literals heuristics (We assume that the tree construction time is negligible comparing to the solving time in our evaluations). Specifically, using the rules of double negations and De Morgan's Law, we move the negation nodes further down as parents of leaf nodes. Then, we can determine if a node is pure positive or not and if it is pure negative or not.

In the solver, we enforce early terminations and unit clauses. Specifically, we simplify the list representation of SAT formulas as we assign values to the variables in the formulas recursively. If the simplified logic is True at any time, we return any possible assignment (if only one solution is needed) or keep track of the solutions (if multiple is need). If the simplified logic is False, we backtrack early before the variables run out. Otherwise, we keep simplifying the formula through the search space until we run out variables and backtrack appropriately. The simplifications are based on rules of early terminations and unit clauses. The also prioritizes any assignment to True for pure positive variables.

In the solver file, we also offer options to try out the naive recursive backtracking implementation of the solver. The user can do so by setting `heuristic_enabled` to False in the `solve` function in `/dpll/solver.py`.
 		
### Usage of SAT Solving: ROBDD
In this section, we will discuss the Reduced-Ordered Binary Decision Diagram (ROBDD) and how to use the ROBDD tool we have created. ROBDD provides an ordered canonical form of logic representation and is an improvement over Binary Decision Trees (BDTs). Different parameter orderings can lead to different versions of ROBDDs for the same logic formula. The complexity and memory consumption of a ROBDD depend not only on the number of parameters but also on their ordering.

In the EduSAT tool, we provide implementations of both BDT and ROBDD and demonstrate the process of reducing a BDT by building its corresponding ROBDD. The base implementation of BDT and ROBDD is located in the `/bdd` directory. To run the interactive user interface for BDT and ROBDD, go to `main.py` and select option `3` for BDDs. The main function will redirect you to the `/bdd/robdd_kernel.py` script and generate user prompts for three additional use cases.

- The **first** option allows the user to input custom logic formulas. To input a legal logic formula, the user must follow the template we have defined above. **Please note that the minimum parameter/variable ordering must be 0 and match the actual parameters in the formula you have entered for the script to work.** We are working on improving error checking and assertions to prevent illegal inputs. Based on the user input, we generate a BDT and an ROBDD with the root node specified by the user.

- The **second** option allows the user to try our framework with pre-defined examples. This option enables the user to explore what is offered in the ROBDD kernel quickly. Specifically, we provide an example and two ways of ordering the parameters. For each ordering, we generate a truth table and a graph visualization.

- The **third** option evokes a script located at `/bdd/robdd_logic_generate.py` to first randomly generate a formula, then construct the corresponding BDT and ROBDD. The user will be prompted to enter the number of parameters, parameter ordering, and depth of the formula. Please note that here, the depth of a logic formula is defined as the number of nested connections (with $\wedge$ or $\vee$).

The workflow behind building BDTs and ROBDDs is as follows:
- when we receive a legal logic formula and an acceptable parameter ordering, the kernel first parses the formula, then calls the `construct_obdd(ordering, logic, vis)` function, where `ordering` specifies the parameter ordering, `logic` specifies the logic expression, and `vis` specifies whether to generate a truth table. 
- Next, we initialize a **graph** data structure that we refer to later for ROBDD. We then call the function `convert_robdd_graph(obdd, g)`, where `obdd` is the ordered BDT constructed in the previous step, and `g` is the ROBDD graph object. 
- The function `convert_robdd_graph(obdd, g)` modifies the graph object directly, which is further reduced using the `g.reduce()` method. Finally, we generate visualizations of ROBDDs using the Python `networkx` library. Note that we are working on interactive visualizations of ROBDD.
- The implementation of solving SAT problems with ROBDD is located at `/SMT_Solver/smt.py` in the function `solve_SMT_ROBDD`. The underlying logic for finding solutions is implemented at `/bdd/robdd_solver.py` in the function `solve`.

We encourage users to refer to our paper for more theoretical discussions on BDT and ROBDD.

## Tests
To test out the programs, please run the files in the /tests sub-directory. The users are encouraged to create more tests on their own to facilitate the familiarity with the framework. If you notice any issues when testing, please contact yiqi.zhao@vanderbilt.edu. For details on comparing different solvers and more details on the theories, please refer to the report attached with this repository.

## Important notes
1. If the SAT logic generator takes forever to generate logics, it is possible that the number of depths is too small comparing to the number of variables, leading to impossible generation of SAT formula(s) that meet the requirement.
2. In the natural language interface, each SMT atom must start with y. For instance a valid SMT clause is y1 + 1 = 2. On the other hand, each SAT atom must start with x. For instance a valid SAT clause is (x1 and x2).

## Acknowledgements
Throughout the tutorial and the codes for this project, we used some materials from the lecture slides provided by Professor Taylor Johnson from CS 6315. More acknowledgements are in the comments of the codes.
