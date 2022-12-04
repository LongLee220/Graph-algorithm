import numpy as np
def product_wise(x,y):
    Z = []
    for i in range(x.shape[0]):
        Z.append(x[i]+y[i])
    return min(Z)


flag = True

A = np.array([[0,10,5,99,99],[99,0,2,1,99],[99,3,0,9,2],[99,99,99,0,4],[7,99,99,6,0]])

while flag == True:
    
    
    B = np.zeros(A.shape)
    for m in range(A.shape[0]):
        X = A[m]
        for n in range(A.shape[1]):
            Y = A[:,n]
            
            z = product_wise(X,Y)
            
            
            if z < A[m,n]:
                B[m,n] = z
            else:
                B[m,n] = A[m,n]
    print(B)
    if (A==B).all():
        flag = False
    else:
        A = B
        flag = True
