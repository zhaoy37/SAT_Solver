from bdd.robdd_graph import OBDD_node, ROBDDNode
from shared.logic_parser import parse_logic
import matplotlib.pyplot as plt
from bdd.logic_eval import eval
import networkx as nx
import numpy as np
import copy


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
    Nicely print the result of an OBDD given a root.
    An additional option to print ascii truth table.
    """
    path = list(allPaths(obdd_root))
    if truth_table:
        print_truth_table(path, ordering)
    else:
        [print(p, end='\n') for p in path]



def construct_obdd(ordering, logic, vis=False):
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
    truth_table = True
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
        if not g.has_node(curr_node):
            g.add_node(curr_node)
        return curr_node
    else:
        left = convert_robdd_graph(obdd.left, g)
        right = convert_robdd_graph(obdd.right, g)
        llst = list(left.path)
        rlst = list(right.path)
        l_one = g._one_connect(left)
        r_one = g._one_connect(right)
        if l_one:
            llst = list(l_one.path)
        if r_one:
            rlst = list(r_one.path)
        llst.insert(0, obdd.val['l'][obdd.var])
        rlst.insert(0, obdd.val['r'][obdd.var])
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
        
