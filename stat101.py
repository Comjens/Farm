import numpy as np
import pandas as pd
from fractions import Fraction
from IPython.display import display, HTML
import matplotlib.pyplot as plt
from math import log2


def PCA(data,IO):
    corr = data.corr()
    eigen = np.linalg.eig(corr)
    if IO==1:
        
        print("Correlation Matrix")
        display(corr)
        print("PCA")
        print("Eigenvalues of correlation matrix")
        PCA = np.array([eigen[0],eigen[0].cumsum(),eigen[0]/(eigen[0].sum()),(eigen[0]/(eigen[0].sum())).cumsum()]).T
        display(pd.DataFrame(PCA,columns = ("Eigen Value","cumative sum","Proportion","Cumulative")))
        display(pd.DataFrame(eigen[1],columns=list(data)))
    
        plt.plot([x for x in range(1,1+len(eigen[0]))],(eigen[0]/(eigen[0].sum())).cumsum(), label='Culmatie', lw=2, marker='o')
        plt.plot([x for x in range(1,1+len(eigen[0]))],1-(eigen[0]/(eigen[0].sum())).cumsum(), label='Missing var', lw=2, marker='s')
        plt.grid()
        plt.legend(loc='upper right')
        plt.title("PCA") 
        plt.show()
    if IO!=0:
        return corr,eigen
    
def testPCA(data,m,IO):
    eigen =  PCA(data,2)
    #test on PCA
    k=len(eigen[0])
    n=len(data)
    np=n-m-1/6*(2*(k-m)+1+2/(k-m))
    Z_1=-np*log2(sum(eigen[0][m:])/(sum(eigen[0])/(k-m)**(k-m)))
    Z_2=-n*log2(sum(eigen[0][m:])/(sum(eigen[0])/(k-m)**(k-m)))
    print("n' = {0}-{1}-1/6*(2*({2}-{1})+1+2/({2}-{1})={3}".format(len(data),m,k,np))
    print("Z_1 = -{0:.3}*log2({1:.3}/({2:.3})/({3}-{4})^({3}-{4})))={5}".format(np,sum(eigen[0][m:]),sum(eigen[0]),k,m,Z_1))
    print("Z_2 = {0}*log2({1:.3}/({2:.3})/({3}-{4})^({3}-{4})))={5}".format(n,sum(eigen[0][m:]),sum(eigen[0]),k,m,Z_2))

def varimax(Phi, gamma = 1, q = 20, tol = 1e-6):
    #from numpy import eye, asarray, dot, sum, diag
    from numpy.linalg import svd
    p,k = Phi.shape
    R = eye(k)
    d=0
    for i in range(q):
        d_old = d
        Lambda = np.dot(Phi, R)
        u,s,vh = svd(dot(Phi.T,np.asarray(Lambda)**3 - (gamma/p) * np.dot(Lambda, np.diag(np.diag(np.dot(Lambda.T,Lambda))))))
        R = np.dot(u,vh)
        d = sum(s)
        if d/d_old < tol: break
    return np.dot(Phi, R)