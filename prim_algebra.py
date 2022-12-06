import numpy as np

A = np.array([[99,7,99,5,99,99,99],[7,99,8,9,7,99,99],[99,8,99,99,5,99,99],[5,9,99,99,15,6,99],[99,7,5,15,99,8,9],[99,99,99,6,8,99,11],[99,99,99,99,9,11,99]])

Nodes = np.arange(A.shape[1])
N = len(Nodes)
ini = 0
d = np.zeros(N)
d[ini] = 0

S = list(Nodes)
S.remove(ini)

for node in S:
    d[node] = 99
Q = []
Q.append(ini)

while len(S) != 0 :
    u = Q[-1]
    for i in S :
        if d[i] > A[u][i] :
            d[i] = A[u][i]
    print(d)
    ID = {}
    for j in S:
        ID[j] = d[j]
    
    v = min(ID,key=ID.get)
    
    Q.append(v)
    S.remove(v)
    print(v)
    
