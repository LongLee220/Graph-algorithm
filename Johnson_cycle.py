#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 19:01:55 2022

@author: longlee
"""


import networkx as nx
from collections import defaultdict



def simple_cycles(G):
    def _unblock(thisnode):
        """Recursively unblock and remove nodes from B[thisnode]."""
        if blocked[thisnode]:
            blocked[thisnode] = False
            while B[thisnode]:
                _unblock(B[thisnode].pop())

    def circuit(thisnode, startnode, component):
        closed = False # set to True if elementary path is closed
        path.append(thisnode)
        blocked[thisnode] = True
        for nextnode in sorted(component[thisnode]): # direct successors of thisnode
            if nextnode == startnode:
                result.append(path + [startnode])
                closed = True
            elif not blocked[nextnode]:
                if circuit(nextnode, startnode, component):
                    closed = True
        if closed:
            _unblock(thisnode)
        else:
            for nextnode in component[thisnode]:
                if thisnode not in B[nextnode]: # TODO: use set for speedup?
                    B[nextnode].append(thisnode)
        path.pop() # remove thisnode from path
        return closed

    path = [] # stack of nodes in current path
    blocked = defaultdict(bool) # vertex: blocked from search?
    B = defaultdict(list) # graph portions that yield no elementary circuit
    result = [] # list to accumulate the circuits found
    # Johnson's algorithm requires some ordering of the nodes.
    # They might not be sortable so we assign an arbitrary ordering.
    ordering=dict(zip(sorted(G),range(len(G))))
    for s in sorted(ordering.keys()):
        # Build the subgraph induced by s and following nodes in the ordering
        subgraph = G.subgraph(node for node in G 
                              if ordering[node] >= ordering[s])
        # Find the strongly connected component in the subgraph 
        # that contains the least node according to the ordering
        strongcomp = nx.strongly_connected_components(subgraph)
        mincomp=min(strongcomp, 
                    key=lambda nodes: min(ordering[n] for n in nodes))
        component = G.subgraph(mincomp)
        if component:
            # smallest node in the component according to the ordering
            startnode = min(component,key=ordering.__getitem__) 
            for node in component:
                blocked[node] = False
                B[node][:] = []
            dummy=circuit(startnode, startnode, component)

    return result


G = nx.DiGraph()
G.add_edge(1,2)
G.add_edge(1,5)
G.add_edge(2,3)
G.add_edge(3,2)
G.add_edge(3,1)
G.add_edge(3,4)
G.add_edge(3,6)
G.add_edge(4,5)
G.add_edge(5,2)
G.add_edge(6,4)


res = simple_cycles(G)

for c in res:
    print (c)
