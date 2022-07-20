#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 14:22:17 2021

@author: longlee
"""


import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
#读入有向图转为无向图G
f = open("0.edges", "r")
lines = f.readlines()
f.close()
G = nx.DiGraph()
G = G.to_directed()
nx.draw(G, pos=nx.spectral_layout(G),node_size=14,node_color= "r", edge_color= "b")
plt.show()
for line in lines:
    tmp = line.strip().split(' ')#把分隔号抹去
    G.add_edge(int(tmp[0]), int(tmp[1]))
A = nx.to_numpy_matrix(G) #创建图的邻接矩阵
n = A.shape[0]
I = np.identity(n)
G = A + I
V_list = list(np.arange(n))#创建点列表
v = np.zeros(n)
v[0] = 1                  #检索的初始节点0对应的向量
component =[]           #component的列表
Adj = set()             #在G.T存储检索节点的BFS搜索结
tmp = 0
while tmp < 8:
    v = np.matmul(G.transpose(), v.reshape(-1,1))
    for i in range(n):
        if v[i][0] != 0:
            Adj.add(i)

    tmp = tmp + 1