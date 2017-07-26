import math
#------- test palindrome-------------
txt='je suis inverse'
n=len(txt)
txt2=''
for i in range(n-1,0,-1):
    txt2+=txt[i]

#------- test complexe-------------

z=complex(2,2)
ze=complex(3,5)

#formulaire:
def addpuiss(a,b,n):
    r=0
    for k in range(0,n+1):
        C=math.factorial(n)/(math.factorial(k)*math.factorial(n-k))
        r+=C*math.pow(b,n-k)*math.pow(a,k)
    return r

def rempuiss(a,b,n):
    r=0
    for k in range(0,n+1):
        C=math.factorial(n)/(math.factorial(k)*math.factorial(n-k))
        r+=C*math.pow(-b,n-k)*math.pow(a,k)
    return r
#-------------------------------------------------------------------------

import numpy as np
import matplotlib as plt

#-----------Systeme neuronale---------------------
wi=[0.1,0.2,0.3,0.4]
xi=[3,6,2,5]
def ADALINE(w,x):#ADAptive LInear NEuron :equation neurone sans seuil de tolerance
    if len(w)!=len(x):
        return "nombre d'entrées et nombre de ponderations differents!"
    p=0
    for i in range(0,len(w)):
        p+=w[i]*x[i]
    return p
"""    
def quadratic_error(y,yd): #y resultat de la fct, yd resultat attendu
    e=y-yd
    return (e*e)/2 #la moitié du carré de la difference entre theorie et pratique
"""

def sigmoide(p):#fonction d'activation du neurone
    N=1/(1+np.exp(-p))s
    return N
def neurosisAF(SP):#lineaire
    return sp
    

if __name__ =="__main__":
    
    print txt2
    print z, ze, z**2, ze**2


