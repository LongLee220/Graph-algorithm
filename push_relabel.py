
import numpy as np
import networkx as nx
import copy
A = np.array([[0,19,13,0,0,0],[0,0,8,12,0,0],[0,4,0,0,10,0],[0,0,9,0,0,25],[0,0,0,14,0,4],[0,0,0,0,0,0]])

#Dic_nodes = {'S':0,'A':1,'B':2,'C':3,'D':4,'t':5}



G = nx.DiGraph()

G.add_edge('S', 'A',weight = 19,flow =0)
G.add_edge('S', 'B',weight = 13,flow =0)
G.add_edge('A', 'B',weight = 8,flow =0)
G.add_edge('A', 'C',weight = 12,flow =0)
G.add_edge('B', 'A',weight = 4,flow =0)
G.add_edge('B', 'D',weight = 10,flow =0)
G.add_edge('C', 'B',weight = 9,flow =0)
G.add_edge('C', 't',weight = 25,flow =0)
G.add_edge('D', 'C',weight = 14,flow =0)
G.add_edge('D', 't',weight = 4,flow =0)
H = G.to_undirected() 


Nodes = list(G.nodes())
ini = 'S'
end = 't'
Hight = {}
Res_flow = {}
for node in Nodes:
    Res_flow[node] = 0
    if node == ini:
        Hight[node] = len(Nodes)
    else:
        Hight[node] = 0
        

for node in G.adj[ini].keys():
    G[ini][node]['flow'] = G[ini][node]['weight']
    Res_flow[node] = G[ini][node]['flow']

Between_flow= {}
for node in Res_flow.keys():
    if node not in [ini,end]:
        Between_flow[node] = Res_flow[node]
        

ini_flow = sum(Between_flow.values())
##1.当前初始流量流出去
nex_between = {}
Flag = True
while Flag == True:
    
    nex_between = copy.deepcopy(Between_flow)
    print('nex_between is the:',nex_between)
    
    for node in Between_flow.keys():
        
        if Res_flow[node] != 0:
             
            t = 0##判断是否能流向邻居节点
            while t == 0:
                
                judge = [] ##判断是否所有邻居节点都走不通
                
                for adj in G.adj[node].keys():
                    e = Res_flow[node] ##当前节点剩余流量
                    print('Resu_flow:',Res_flow)
                    
                    f = G[node][adj]['weight']
                    judge.append(f)
                    
                    if f != 0:#当前节点存在的流量还能流向节点的容量
                    
                        if Hight[node] > Hight[adj]:
                            
                            t+=1
                            print('Flag',t,adj)
                            
                            f = G[node][adj]['weight']
                        
                            if e > f :#当前节点存在的流量大于流向节点的容量
                                
                                Res_flow[node] = e - f
                                G[node][adj]['weight'] = 0
                                G[node][adj]['flow'] = G[node][adj]['flow'] + f
                                
                                if adj == end:
                                    Res_flow[adj] = 0
                                else:
                                    
                                    Res_flow[adj] = Res_flow[adj]+f
                                
                            else:
                                
                                Res_flow[node] = 0
                                G[node][adj]['weight'] = f - e
                                G[node][adj]['flow'] = G[node][adj]['flow'] + e 
                                
                                if adj == end:
                                    Res_flow[adj] = 0
                                else:
                                    
                                    Res_flow[adj] = Res_flow[adj] + e
                            
                
                if t == 0:
                    Hight[node] = Hight[node] + 1
                
                # else:
                if sum(judge) == 0:
                    t = 1
                    Hight[node] = Hight[node] + 1
                # else:
                #     t = 0
                #     Hight[node] = Hight[node] + 1
            
        Between_flow[node] = Res_flow[node]
    print('Between_flow is the:',Between_flow)
    
    if nex_between != Between_flow:
        Flag = True
        print(Flag)
    else:
        Flag = False
        print(Flag)
        
res_flow = sum(Between_flow.values())

max_flow = ini_flow - res_flow
print(max_flow)
    
