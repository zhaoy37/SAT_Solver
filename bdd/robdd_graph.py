"""
Authors: Ziyan An
References: 

Implementations for OBDD, ROBDD structures.
"""

from collections import defaultdict



class OBDD_node(object):
    """
    A simple class for OBDD nodes.
    """
    def __init__(self, var, leaf=False) -> None:
        self.var = var      ## variable ordering
        self.val = None     ## keys: 'l', 'r'; vals: [(variable ordering, truth value)]
        self.left = None    ## low child 
        self.right = None   ## high child
        self.leaf = leaf    ## if is a leaf

    def __eq__(self, other):
        """
        Evaluate equality for two OBDD nodes. 
        Two nodes are considered equal if they have the same path and the same value.
        """
        if isinstance(other, OBDD_node):
            return (self.val == other.val and 
                    self.var == other.var and 
                    self.leaf == other.leaf)
        return False



class ROBDDNode:
    """
    A ROBDD graph node. 
    """
    def __init__(self, var, path=None):
        self.var = var
        self.path = path

    def __eq__(self, other):
        """
        Evaluate equality for two ROBDD nodes. 
        Two nodes are considered equal if they have the same path and the same value.
        """
        if isinstance(other, ROBDDNode):
            return (self.path == other.path and self.var == other.var)
        return False
    
    def __hash__(self):
        """
        Hash function for ROBDD nodes by id.
        """
        return id(self)



class ROBDD_graph(object):
    """
    A class for ROBDD graph representation.
    """
    def __init__(self, directed=True, init_val=0):
        self._graph = {}            ## keys: node; values: references to node
        self._directed = directed   ## ROBDD is represented as a directed graph
        self.init_val = init_val    ## variable that ROBDD starts from

    def has_node(self, test_node):
        """
        Input: an ROBDD node object.
        Returns if a node already exists in the ROBDD.
        """
        for k in self._graph.keys():  
            if test_node == k:
                return k
        return False
    
    def add_node(self, node):
        """
        Add a node to ROBDD graph.
        Initialize the reference as an empty list.
        """
        self._graph[node] = []

    def connected(self, node1, node2):
        """
        Inputs: two ROBDD nodes.
        Returens True if node2 is in the reference list of node1. 
        """
        if node2 in self._graph[node1]:
            return True
        return False
    
    def _one_connect(self, node):
        """
        Test 1. if the node is included in the graph;
        2. if the node the connected to only one child.
        """
        ref = self.has_node(node)       ## test if the node is in the graph.
        if len(self._graph[ref])==1 and self._graph[ref][0].var == -1:
            return self._graph[ref][0]
        else:
            return False
        
    def reduce(self):
        """
        Reduce an ROBDD graph such that there are no repeat nodes. 
        """
        all_nodes = self._graph.keys()
        all_refs = self._graph.values()
        unique_n = set(all_nodes)
        unique_r = list(set(sum(all_refs, [])))
        to_delete = unique_n.difference(unique_r)
        for d in to_delete:
            if d.var != self.init_val:
                del self._graph[d]
        single_connect_node = {}
        for k, v in self._graph.items():
            if k.var >= 0 and len(v) == 1:
                single_connect_node[k] = v[0]
        for k, v in self._graph.items():
            self._graph[k] = [single_connect_node[ci] if ci in single_connect_node else ci for ci in v]
        for k in single_connect_node.keys():
            del self._graph[k]
        

    def connect(self, node1, node2):
        """
        Inputs: two ROBDD nodes.
        Connects two ROBDD nodes.
        """
        if self._one_connect(node2):
            self._graph[node1].append(self._one_connect(node2))
        else:
            ref = self.has_node(node2)
            self._graph[node1].append(ref)

        if not self._directed:  
            if self._one_connect(node1):
                self._graph[node2].append(self._one_connect(node1)) 
            else:
                ref = self.has_node(node1)
                self._graph[node2].append(ref)

