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



class ROBDDNode:
    """
    A ROBDD graph node. 
    """
    def __init__(self, var, path=None):
        self.var = var
        self.path = path

    def __eq__(self, other):
        if isinstance(other, ROBDDNode):
            return (self.path == other.path and self.var == other.var)
        return False
    
    def __hash__(self):
        return id(self)



class ROBDD_graph(object):
    """
    A class for ROBDD graph representation.
    """
    def __init__(self, directed=True):
        self._graph = {}
        self._directed = directed

    def has_node(self, test_node):
        for k in self._graph.keys():
            if test_node == k:
                return k
        return False
    
    def add_node(self, node):
        self._graph[node] = []

    def connected(self, node1, node2):
        if node2 in self._graph[node1]:
            return True
        return False
    
    def _one_connect(self, node):
        ref = self.has_node(node)
        if len(self._graph[ref])==1 and self._graph[ref][0].var == -1:
            return self._graph[ref][0]
        else:
            return False
        
    def reduce(self):
        all_nodes = self._graph.keys()
        all_refs = self._graph.values()
        unique_n = set(all_nodes)
        unique_r = list(set(sum(all_refs, [])))
        to_delete = unique_n.difference(unique_r)
        for d in to_delete:
            if d.var != 0:
                del self._graph[d]

    def connect(self, node1, node2):
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

