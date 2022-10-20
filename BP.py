#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 09:19:17 2022

@author: longlee
"""

import networkx as nx

from networkx.algorithms import bipartite
import copy

import matplotlib.pyplot as plt 
import matplotlib as mpl
B = nx.Graph()
# Add nodes with the node attribute "bipartite"
B.add_nodes_from(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'], bipartite=0)
B.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], bipartite=1)
# Add edges only between nodes of opposite node sets
B.add_edges_from([('a', 3), ('a', 6), ('a', 7),('a', 8), ('b', 1), ('b', 2), ('b', 5), ('b', 12), ('c', 4), ('c', 9), ('c', 10), ('c', 11), ('d', 2), ('d', 6), ('d', 7), ('d', 10), ('e', 1), ('e', 3), ('e', 8), ('e', 11), ('f', 4), ('f', 5), ('f', 9), ('f', 12), ('g', 1), ('g', 4), ('g', 5), ('g', 9), ('h', 6), ('h', 8), ('h', 11), ('h', 12), ('i', 2), ('i', 3), ('i', 7), ('i', 10)])

X = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
Y = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
Edges = []#[('a', 3), ('a', 6), ('a', 7),('a', 8), ('b', 1), ('b', 2), ('b', 5), ('b', 12), ('c', 4), ('c', 9), ('c', 10), ('c', 11), ('d', 2), ('d', 6), ('d', 7), ('d', 10), ('e', 1), ('e', 3), ('e', 8), ('e', 11), ('f', 4), ('f', 5), ('f', 9), ('f', 12), ('g', 1), ('g', 4), ('g', 5), ('g', 9), ('h', 6), ('h', 8), ('h', 11), ('h', 12), ('i', 2), ('i', 3), ('i', 7), ('i', 10)]
pos = dict()
pos.update( (n, (1, i)) for i, n in enumerate(X) )
pos.update( (n, (2, i+1)) for i, n in enumerate(Y) )
nx.draw_networkx_nodes(B, pos, nodelist=X, node_color='slategray',alpha=0.95, node_size = 350)
nx.draw_networkx_nodes(B, pos, nodelist=Y, node_color='steelblue',alpha=0.95, node_size = 350)
nx.draw_networkx_labels(B,pos)


edges = nx.draw_networkx_edges(B, pos = pos, edge_color = 'black',
        width=1.5, edge_cmap=plt.cm.Blues, edge_vmin = 0, alpha=0.9)
pc = mpl.collections.PatchCollection(Edges, cmap=plt.cm.Blues)

plt.colorbar(pc)
ax = plt.gca()
ax.set_axis_off()
plt.show()

bottom_nodes, top_nodes = bipartite.sets(B)

check_nodes, variable_nodes = bipartite.sets(B)

obtained = {1:0.9,2:0.5,3:0.4,4:0.3,5:0.9,6:0.9,7:0.9,8:0.9,9:0.9,10:0.9,11:0.9,12:0.9}

Score_1 = {}
Score_0 = {}

    
for VN in variable_nodes:
    tmp_1 = {}
    tmp_0 = {}
    for node1 in list(B[VN]):
        tmp_1[node1] = obtained[VN]
        tmp_0[node1] = 1-obtained[VN]
        
    Score_1[VN] = tmp_1
    Score_0[VN] = tmp_0

    

def Decoder(bottom_nodes, top_nodes, Score_1, Score_0):
    

    ##Check_Nodes decoder
    decoder_ch = {} #{V1:{C_1:score_1,C_2:score_2,...},...,Vi:{C_i:score_i,C_j:score_j,...},...}
    
    for VN in top_nodes:

        decoder_tmp_ch = {}
        for node1 in list(B[VN]):

            
            Nei = list(B[node1])

            Nei.remove(VN)

            tmp = 1
            for node2 in Nei:
                 
                tmp = tmp*(1-2*Score_1[node2][node1])
            cv_score = 1/2*(1 - tmp)
            decoder_tmp_ch[node1] = cv_score
    
        decoder_ch[VN] = decoder_tmp_ch
    
    
    ##Variable_Nodes decoder
    decoder_va = {} #{C1:{V_1:score_1,V_2:score_2,...},...,Ci:{V_i:score_i,V_j:score_j,...},...}
    
    for CN in bottom_nodes:
        
        decoder_tmp_va = {}
        for node1 in list(B[CN]): 
            Nei = list(B[node1])

            Nei.remove(CN)
            
            tmp_1 = Score_1[node1][CN]
            tmp_0 = Score_0[node1][CN]
            for node2 in Nei:
                tmp_1 = tmp_1*decoder_ch[node1][node2]
                tmp_0 = tmp_0*(1-decoder_ch[node1][node2])
                
            decoder_tmp_va[node1] = tmp_1/(tmp_1+tmp_0)
        decoder_va[CN] = decoder_tmp_va
    
    
    ##conclusion decoder information
    Con_ino_1 = {}
    Con_ino_0 = {}
    for VN in top_nodes:
        tmp_1 = {}
        tmp_0 = {}
        for CN in bottom_nodes:
            for key in decoder_va[CN].keys():
                
                if key == VN:
                    tmp_1[CN] = decoder_va[CN][key]
                    tmp_0[CN] = 1 - decoder_va[CN][key]
                    
        Con_ino_1[VN] = tmp_1
        Con_ino_0[VN] = tmp_0
    
    Score_1 = copy.deepcopy(Con_ino_1)
    Score_0 = copy.deepcopy(Con_ino_0)
    
   
    return decoder_ch, Score_1, Score_0

# def Draw(Target):
    


Date = {}
for VN in variable_nodes:
    Date[VN] = list()
    Date[VN].append(obtained[VN])


    
ite = 6
t = 0
while t < ite:
    
    decoder_ch, Score_1, Score_0 = Decoder(bottom_nodes, top_nodes, Score_1, Score_0)
    
    Up = copy.deepcopy(decoder_ch)
    Down = copy.deepcopy(Score_1)
    
    for VN in Up.keys():
        
        for CN in Up[VN]:
            Date[VN].append(Up[VN][CN])
    
    for VN in Down.keys():
        
        for CN in Down[VN]:
            Date[VN].append(Down[VN][CN])
    
    t = t+1



        
                 
             
             