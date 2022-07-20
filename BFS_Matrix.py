#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 09:38:20 2021

@author: longlee
"""

import numpy as np
import networkx as nx
import scipy.sparse as sp
import time
import copy

G = nx.DiGraph()

# import matplotlib.pyplot as plt
# f = open("0.edges", "r")  #读入无向图G
# lines = f.readlines()
# f.close()

# nx.draw(G, pos=nx.spectral_layout(G),node_size=14,node_color= "r", edge_color= "b")
# plt.show()
# for line in lines:
#     tmp = line.strip().split(' ')#把分隔号抹去
#     G.add_edge(int(tmp[0]), int(tmp[1]))
t_0 = time.time()

f = open("/Users/longlee/Downloads/gre_512 2/gre_512.mtx")
rows = []
cols = []
vals = []

while True:
    
    line = f.readline()
    tmp = line.strip().split(' ')#把分隔号抹去
    
    if len(tmp) > 1 and  '%' not in tmp[0]:
        G.add_edge(int(tmp[0]), int(tmp[1]))
        rows.append(int(tmp[0]))
        cols.append(int(tmp[1]))
        vals.append(int(1))
        
    
    if not line:
        break
f.close()

e_0 = time.time()

# G.add_edge(0, 1)
# G.add_edge(0, 4)
# G.add_edge(0, 7)
# G.add_edge(1, 2)  
# G.add_edge(1, 6)
# G.add_edge(1, 8)
# G.add_edge(2, 0)
# G.add_edge(2, 1)
# G.add_edge(2, 3)
# G.add_edge(2, 5)
# G.add_edge(3, 4)
# G.add_edge(4, 1)
# G.add_edge(5, 3)
# G.add_edge(7, 8)
# G.add_edge(8, 7)



# rows = [0,0,0,1,1,1,2,2,2,2,3,4,5,7,8]
# cols = [1,4,7,2,6,8,0,1,3,5,4,1,3,8,7]
# vals = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

n = 513


A = sp.coo_matrix((vals, (rows,cols)),shape = (n, n))

I = np.identity(n)
A = A + I
b = np.ones(n)
D = A.dot(b)
D = D.tolist()
D = D[0]

###
def BFS_M(M,Checked,V,Adj,tmp,Scc,Node):
    # Node = set(Node).difference(Scc)
    # V_N = copy.deepcopy(Node)
    Flag = True
    while Flag == True:
        bfs_tmp = []
        
        # # V = np.dot(M, V)
        v_c = np.zeros((n,1))
        for i in list(Adj[tmp]):
            v_c = v_c + M[:,i]
        V = v_c
        
        
        # key = list(Adj.keys())[-1]
        # Res = set(Node).difference(set(Adj[key]))
        # V_N = set(V_N).difference(set(Adj[tmp]))
        # for i in V_N:
        Res = set(Node)-Checked
        # Res = copy.deepcopy(V_N)
        for i in Res:
            if V[i] != 0 :
                Checked.add(i)
                # V[i]= 1
                bfs_tmp.append(i)
                # V_N.remove(i)
        if len(bfs_tmp) != 0:
            tmp = tmp +1
            Adj[tmp] = bfs_tmp
            Flag = True
        else:
            Flag = False
    
    return(Checked)

# V_l = list(np.arange(n))#创建点列表
# ini_node = V_l[0]
# v = np.zeros((n,1))
# v[ini_node] = 1
# Check1 = set()
# Check1.add(ini_node)

# GT_bfs = BFS_M(A.T,Check1,v)


def Com_M(A, V_list, N):
    Com = {}
    SSC = set()
    tmp = 0
    # b = np.ones((N,1))
    # # D = A.dot(b)
    # # # D = D.tolist()
    # print(D)
    while len(V_list) !=0:
        
        ini_node = D.index(max(D)) #V_list[0]
        v = np.zeros((N,1))
        v[ini_node] = 1
        Adj1 = {}
        Adj1[0] = [ini_node]
        v1 = np.zeros((N,1))
        v1[ini_node] = 1
        Check1 = set()
        Check1.add(ini_node)
        Check2 = set()
        Check2.add(ini_node)
        Adj2 = {}
        Adj2[0] = [ini_node]
        
        GT_bfs = BFS_M(A.T,Check1,v,Adj1,tmp = 0,Scc = SSC,Node = V_list)

        G_bfs = BFS_M(A,Check2,v1,Adj2,tmp = 0,Scc = SSC,Node = V_list)
        
        com = GT_bfs.intersection(G_bfs)
        
        for ide in com:
            D[ide] = 0
            
        SSC = SSC|com
        Com[tmp] = com
        tmp = tmp + 1
        V_list = set(V_list)-com
        
    return(Com,tmp)

t1 = time.time()
V_l = set(np.arange(n))#创建点列表
TT = Com_M(A,V_l,n)
Com_1 = TT[0]
print('tmp: ', TT[1])
e1 = time.time()
print('M-Com time is: ', (e1-t1)/2)

# t2 = time.time()
# Com_2 = list(nx.strongly_connected_components_recursive(G))
# e2 = time.time()
# print('Tarjan recursive time is:', e2-t2 + e_0-t_0)

t3 = time.time()
Com_3= list(nx.kosaraju_strongly_connected_components(G))
e3 = time.time()
print('kosaraju time is:', e3-t3 + e_0-t_0)

t4 = time.time()
Com_4 = list(nx.strongly_connected_components(G))
e4 = time.time()
print('Tarjan time is: ', e4-t4 + e_0-t_0)


# Cycle = {}
# for i in range(len(Com_1)):
#     filter_node = list(Com_1[i])
#     H = G.subgraph(filter_node)

    
#     cycles = list(nx.simple_cycles(H))
#     for cycle in cycles:
#         if len(cycle) < 3:
#             cycles.remove(cycle)
#     if len(cycles) > 0:
        
#         Cycle[i] = cycles
       

'''
#BFS + DFS
t5 = time.time()
L = 7
Cycle_1 = {}
for i in range(len(Com_1)):
    
    filter_node = list(Com_1[i])
    
    cycle = []
    while len(filter_node) >= 3:
        
        H = G.subgraph(filter_node)
        f_node = filter_node[0]

        que = []
        que.append(f_node)
        Que = []
        Que.append(que)
        
        while len(Que) != 0:
            print(len(filter_node))
            print(len(Que))
            Que_t = []
            for que in Que:
                
                # que = Que[i]
                
    
                if len(que) > L:
                    Que.remove(que)
                else:
                    node = que[-1]
                    Res = list(set(H[node]).difference(set(que)))
                    
                    
                    
                    for adj_node in Res:
                        tmp = []
                        tmp = copy.deepcopy(que)
                        
                        if adj_node not in que:
                            tmp.append(adj_node)
                            
                            Que_t.append(tmp)
                            
                            if f_node in H[adj_node] and len(tmp) >2:
                                cycle.append(tmp)
                                
            Que = Que_t
        filter_node.remove(f_node)
    if len(cycle) >0:
        
        Cycle_1[i] = cycle
e5 = time.time()
print(e5-t5)
'''