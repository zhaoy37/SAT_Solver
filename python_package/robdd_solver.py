"""
Authors: Ziyan An
References:

Implementation for the main OBDD, ROBDD solver.
"""
import sys
sys.path.append('..')
from .robdd_graph import OBDD_node, ROBDDNode, ROBDD_graph
from .rodbb_visualization import view_rodbb
from .logic_parser import parse_logic
import matplotlib.pyplot as plt
from .logic_eval import eval
from .calculator import calculate
import networkx as nx
import numpy as np
import copy
import timeit
import itertools
import networkx as nx


def allPaths(node):  
    """
    List every path of an OBDD tree structure.
    """
    if node:
        if not node.left and not node.right:
            yield [node.val]
        else:
            yield from (arr for arr in allPaths(node.left))
            yield from (arr for arr in allPaths(node.right))



def print_truth_table(path, ordering):
    """
    Print an ascii style truth table for an OBDD path.
    """
    np_rep = np.array(path)     ## a np array representation
    np_rep = np.squeeze(np_rep, axis=1)
    print('|', end=' ')
    for i in range(np_rep.shape[1]-1):
        print('x'+str(ordering[i])+' |', end=' ')
    print('truth value |')
    print('-' * (5*(np_rep.shape[1]-1)+15))
    for i in range(np_rep.shape[0]):
        print('|', end=' ')
        for j in range(np_rep.shape[1]-1):
            print(' '+str(np_rep[i,j,1])+' |', end=' ')
        print('      '+str(np_rep[i,-1,1]), end='     |\n')



def print_obdd(obdd_root, ordering, truth_table=False):
    """
    Nicely present the result of an OBDD given a root.
    An additional option to print ascii truth table.
    """
    path = list(allPaths(obdd_root))
    if truth_table:
        print_truth_table(path, ordering)
    else:
        [print(p, end='\n') for p in path]



def construct_obdd(ordering, logic, vis=False, truth_table=True):
    """
    Construct an OBDD from a given ordering and a logic expression.
    """
    obdd = OBDD_node(var=ordering[0])
    obdd.val = {    
        "l": [(ordering[0],0)],   ## [(variable, truth value)]
        "r": [(ordering[0],1)],   ## [(variable, truth value)]
    }
    node_ls = [obdd]              ## a list of nodes 
    while len(node_ls) < 2**(len(ordering)-1):
        curr_node = node_ls.pop(0)
        curr_var = ordering[ordering.index(curr_node.var)+1]
        curr_node.left = OBDD_node(var=curr_var)
        curr_node.left.val = {
            "l": copy.copy(curr_node.val["l"]), 
            "r": copy.copy(curr_node.val["l"]),
        }
        curr_node.left.val["l"].append((curr_var, 0))
        curr_node.left.val["r"].append((curr_var, 1))
        curr_node.right = OBDD_node(var=curr_var)
        curr_node.right.val = {
            "l": copy.copy(curr_node.val["r"]), 
            "r": copy.copy(curr_node.val["r"]),
        }
        curr_node.right.val["l"].append((curr_var, 0))
        curr_node.right.val["r"].append((curr_var, 1))
        node_ls.append(curr_node.left)
        node_ls.append(curr_node.right)
    eval_obdd(obdd, logic)              ## add final leaf nodes
    if truth_table and vis:
        print_obdd(obdd, ordering, truth_table=truth_table)  ## check obdd
    return obdd



def eval_obdd(node, logic):
    """
    Evaluate an OBDD given a root node and a logic expression.
    """
    if node:
        if not node.left and not node.right:
            node.left   = OBDD_node(var=-1, leaf=True)
            node.right  = OBDD_node(var=-1, leaf=True)
            left_val    = eval(logic= logic, value= node.val["l"])
            right_val   = eval(logic= logic, value= node.val["r"])
            node.left.val  = copy.copy(node.val["l"])
            node.right.val = copy.copy(node.val["r"])
            node.left.val.append((-1, left_val))
            node.right.val.append((-1, right_val))
        else:
            eval_obdd(node.left, logic)
            eval_obdd(node.right, logic)



def robddPaths(g):  
    """
    List every path of an OBDD tree structure.
    """
    for k, v in g._graph.items():
        print("connect: ")
        print(k.var, k.path)
        [print(vi.var, vi.path, end="\t") for vi in v]
        print("\n")



def convert_robdd_graph(obdd, g):
    if obdd.leaf:
        curr_node = ROBDDNode(var=obdd.var, path=[obdd.val[-1]])
        find_node = g.has_node(curr_node)
        if not find_node:
            g.add_node(curr_node)
        find_node = g.has_node(curr_node)
        return find_node
    else:
        left = convert_robdd_graph(obdd.left, g)    ## returns left node
        right = convert_robdd_graph(obdd.right, g)  ## returns right node
        llst = list(left.path)
        rlst = list(right.path)
        l_one = g._one_connect(left)
        r_one = g._one_connect(right)
        if l_one:
            llst = list(l_one.path)
        if r_one:
            rlst = list(r_one.path)
        l_sert = [t for t in obdd.val['l'] if t[0] == obdd.var][0]
        r_sert = [t for t in obdd.val['r'] if t[0] == obdd.var][0]
        llst.insert(0, l_sert)
        rlst.insert(0, r_sert)
        new_node = ROBDDNode(var=obdd.var, path=[llst, rlst])
        
        find_node = g.has_node(new_node)
        if not find_node:
            g.add_node(new_node)
            find_node = g.has_node(new_node)
            if left == right:
                if not g.connected(find_node, left):
                    g.connect(find_node, left)
            else:
                if not g.connected(find_node, left):
                    g.connect(find_node, left)
                if not g.connected(find_node, right):
                    g.connect(find_node, right)

        return find_node
        


def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result



def replace_val(sat_formula, convertion):
    if type(sat_formula) == str:
        try:
            return convertion[sat_formula]
        except KeyError:
            return sat_formula
    else:
        for i in range(len(sat_formula)):
            sat_formula[i] = replace_val(sat_formula[i], convertion)
        return sat_formula



def check_sat_formula_format(sat_formula):
    if type(sat_formula) == str:
        flatten_ls = [sat_formula]
    else:
        flatten_ls = flatten(sat_formula)

    counter = 0
    for lt in flatten_ls:
        if 'x' in lt:
            counter = max(counter, int(lt[1:]))
    counter += 1
    convertion = {}
    reversed_conv = {}
    for lt in flatten_ls:
        if 'x' not in lt and lt not in ['and', 'or', 'not']:
            convertion[lt] = 'x' + str(counter)
            reversed_conv['x' + str(counter)] = lt
            counter += 1
    
    if len(convertion) != 0:
        sat_formula = replace_val(sat_formula, convertion)
    return sat_formula, convertion, reversed_conv


def solve(sat_formula, get_time=False, multiple=True):
    """
    The input is a parsed logic formula.
    """
    logic = sat_formula
    sat_formula, convertion, reversed_conv = check_sat_formula_format(sat_formula)

    if type(sat_formula) == str:
        flatten_ls = [sat_formula]
    else:
        flatten_ls = flatten(sat_formula)

    variables = []
    for f in flatten_ls:
        if 'x' in f:
            variables.append(int(f[1:]))
    ordering = [i for i in range(max(variables)+1)]
    variables = [*set(variables)]
    
    obdd = construct_obdd(ordering, logic, vis=False)
    start_time = timeit.default_timer()
    g = ROBDD_graph(directed=True, init_val=ordering[0])
    robdd_res = convert_robdd_graph(obdd, g)
    g.reduce()
    G, edge_labels = view_rodbb(g, ordering, view=False, label=True)

    all_node_attr = []
    target_node = None
    for node, attrs in G.nodes.data():
        if G.nodes[node]['color'] == 'blue':
            all_node_attr.append(G.nodes[node]['var'])
        elif G.nodes[node]['var'] == -1:
            target_node = node

    source_node = None
    if len(all_node_attr) < 1:
        source_node = target_node 
    else:
        for node in G.nodes():
            if G.nodes[node]['var'] == min(all_node_attr):
                source_node = node

    # print("target_node", target_node)
    # print("source_node", source_node)
    # for node, attributes in G.nodes.data():
    #     print("Node:", node)
    #     for attr, value in attributes.items():
    #         print(f"{attr}: {value}")
    #     print()
    
    if not target_node and not source_node:
        if get_time:
            return "UNSAT", timeit.default_timer()-start_time
        return "UNSAT"

    paths_to_t = []
    if not multiple:
        try:
            path = nx.shortest_path(G, source_node, target_node)
            paths_to_t.append(path)
        except:
            # print(source_node, target_node)
            # for node in G.nodes(data=True):
            #     print(node)
            # G, edge_labels = view_rodbb(g, ordering, view=True, label=True)
            if get_time:
                return "UNSAT", timeit.default_timer()-start_time
            return "UNSAT"
    else:
        try:
            for path in nx.all_simple_paths(G, source_node, target_node):
                paths_to_t.append(path)
        except:
            if get_time:
                return "UNSAT", timeit.default_timer()-start_time
            return "UNSAT"

    all_solutions = []
    for sol in paths_to_t:
        one_sol = {}
        connections = [(sol[i], sol[i+1]) for i in range(len(sol)-1)]
        for c in connections:
            varb = 'x'+str(G.nodes[c[0]]['var'])
            valu = 1 if edge_labels[c] == 'high' else 0
            one_sol[varb] = valu
        
        missing_var = []
        for var in variables:
            if 'x'+str(var) not in one_sol.keys():
                missing_var.append('x'+str(var))
        
        if len(missing_var) == 0:
            all_solutions.append(one_sol)
        else:
            values = [0, 1]
            filled_sol = list(itertools.product(values, repeat=len(variables)))
            for fs in filled_sol:
                temp_sol = one_sol
                for idx,m in enumerate(missing_var):
                    temp_sol[m] = fs[idx]
                all_solutions.append(temp_sol)
    
    for sol in all_solutions:
        for k, v in reversed_conv.items():
            try:
                ans_val = sol[k]
                sol[v] = ans_val
            except:
                pass

    if get_time:
        return all_solutions, timeit.default_timer()-start_time
    return all_solutions