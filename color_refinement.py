#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 15:15:12 2022

@author: longlee
"""

import numpy as np
import networkx as nx


G1 = nx.Graph()
# G1.add_edge(1,2)
# G1.add_edge(1,4)
# G1.add_edge(1,5)
# G1.add_edge(1,6)
# G1.add_edge(2,3)
# G1.add_edge(2,4)
# G1.add_edge(3,4)
G1.add_edge(1,2)
G1.add_edge(2,3)
G1.add_edge(3,4)
G1.add_edge(4,5)
G1.add_edge(5,6)
G1.add_edge(6,1)
G1.add_edge(4,7)
G1.add_edge(7,8)
G1.add_edge(8,9)
G1.add_edge(9,10)
G1.add_edge(10,5)


G2 = nx.Graph()
# G2.add_edge(1,2)
# G2.add_edge(1,3)
# G2.add_edge(1,4)
# G2.add_edge(1,6)
# G2.add_edge(2,3)
# G2.add_edge(3,4)
# G2.add_edge(4,5)
G2.add_edge(1,2)
G2.add_edge(2,3)
G2.add_edge(3,4)
G2.add_edge(4,5)
G2.add_edge(5,1)
G2.add_edge(4,6)
G2.add_edge(6,7)
G2.add_edge(7,8)
G2.add_edge(8,9)
G2.add_edge(9,10)
G2.add_edge(10,6)

ini_colo_1 = {}

for node in G1.nodes():
    ini_colo_1[node] = str(1)
col_va_1 = {}
col_va_1[str(1)] = len(ini_colo_1.values())


ini_colo_2 = {}
for node in G2.nodes():
    ini_colo_2[node] = str(1)
    
col_va_2 = {}
col_va_2[str(1)] = len(ini_colo_2.values())

Col = {1:[str(1)]}


def col_refinement(G_1,G_2,col_1,col_2,colv_1,colv_2,Col):
    '''

    Parameters
    ----------
    G_1 : Graph1.
    G_2 : Graph2.
    col_1 :{v1:color1,v2:color2,...}.
    col_2 :{vi:colori,vj:colorj,...}.
    colv_1 :{color1:num1,...}.
    colv_2 :{coloro:numi}.
    Col : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    
    #1.聚合颜色
    Nei_col_1 = {}
    for node in G_1.nodes():
        tem = []
        tem.append(col_1[node])
        # tem = col_1[node]
        
        for adj in G_1[node]:
            tem.append(col_1[adj])
        Nei_col_1[node] = tem
        
        
        #将邻居的颜色做到映射里面
        L = []
        for tup_val in list(Col.values()):
            L.append(len(tup_val))
            
        if len(tem) not in L:
            Col[len(Col) +1] = tem
            
        else:
            
            t = 0
            T = 0
            for tup_val in list(Col.values()):
                
                
                if len(tup_val) == len(tem):
                    T += 1
                    
                    if set(tup_val) == set(tem):
                        mui_col = []
                        for ide in range(len(tup_val)):
                            non = tup_val[ide]
                            mui_col.append(tem.count(non)-tup_val.count(non))
                        if mui_col != [0]*len(mui_col):
                                
                            Col[len(Col) +1] = tem
                            break
                    else:
                        t += 1

            if T == t != 0:
                
                Col[len(Col) +1] = tem
                
    # print(Nei_col_1)
    # print(Col)                  
    
    
    Nei_col_2 = {}
    for node in G_2.nodes():
        tem = list()
        tem.append(col_2[node])
        for adj in G_2[node]:
            tem.append(col_2[adj])
        Nei_col_2[node] = tem
        
        L = []
        for tup_val in list(Col.values()):
            L.append(len(tup_val))
            
        if len(tem) not in L:
            Col[len(Col) +1] = tem
            
        else:
            t = 0
            T = 0
            for tup_val in list(Col.values()):
                
                
                if len(tup_val) == len(tem):
                    T += 1
                    
                    if set(tup_val) == set(tem):
                        mui_col = []
                        for ide in range(len(tup_val)):
                            non = tup_val[ide]
                            mui_col.append(tem.count(non)-tup_val.count(non))
                        if mui_col != [0]*len(mui_col):
                                
                            Col[len(Col) +1] = tem
                            break
                    else:
                        t += 1

            if T == t != 0:
                
                Col[len(Col) +1] = tem
                        


    print(Nei_col_1)
    # print(Nei_col_2)
    print(Col)
    
    #2.哈希映射
    for node in G_1.nodes():
        nei = Nei_col_1[node]
        
        for k,v in Col.items():
            
            if len(v) == len(nei):
                
                if set(v) == set(nei):
                    
                    mui_col = []
                    for ide in range(len(v)):
                        non = v[ide]
                        mui_col.append(nei.count(non)-v.count(non))
                    if mui_col == [0]*len(mui_col):
                        
                        col_1[node] = str(k)
                
                
    print('G1:',col_1)  
    for val in Col.keys():
        if str(val) not in colv_1.keys():
            
            colv_1[str(val)] = list(col_1.values()).count(str(val))
    
    for node in G_2.nodes():
        nei = Nei_col_2[node]
        for k,v in Col.items():
            if len(v) == len(nei):
                if set(v) == set(nei):
                    mui_col = []
                    for ide in range(len(v)):
                        non = v[ide]
                        mui_col.append(nei.count(non)-v.count(non))
                    if mui_col == [0]*len(mui_col):
                        
                        col_2[node] = str(k)
        
    for val in Col.keys():
        if str(val) not in colv_2.keys():
            
            colv_2[str(val)] = list(col_2.values()).count(str(val))
            

    return col_1,col_2,colv_1,colv_2,Col



ite = 0
while ite < 4:
    
    ini_colo_1,ini_colo_2,col_va_1,col_va_2,Col = col_refinement(G1,G2,ini_colo_1,ini_colo_2,col_va_1,col_va_2,Col)
    
    ite += 1
    
V1 = np.array(list(col_va_1.values()))

V2 = np.array(list(col_va_2.values()))

prod_1 = np.dot(V1.T,V2) 

prod_true = np.dot(V1.T,V1)   

               
    