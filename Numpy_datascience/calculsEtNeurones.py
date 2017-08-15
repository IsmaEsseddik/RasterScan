# coding: utf-8

import math
import numpy as np
import matplotlib as plt
"""
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
"""


#-----------Systeme neuronale---------------------
wi=[0.1,0.2,0.3,0.4]
xi=[3,6,2,5]
"""
def ada_li_ne(x,w): # ADAptive LInear NEuron :equation neurone sans seuil de tolerance
    assert len(w)== len(x),"nombre d'entrées et nombre de ponderations differents!"
    p=0
    for i in range(0,len(w)):
        p+=w[i]*x[i]
    return p
    
def quadratic_error(y,yd): #y resultat de la fct, yd resultat attendu
    e=y-yd
    return (e*e)/2 #la moiti� du carr� de la difference entre theorie et pratique
"""

def sigmoide(x):  # fonction d'activation du neurone
    s=1/(1+math.exp(-x))
    return s

def Heaviside(x):  # fonction lineaire
    return x

def boolOU(a,b):
    """ retourne une valeur selon un test logique OU, les poids étant paramétré à 1"""
    assert(type(x1)=='bool' and type(x2)=='bool'),"les deux entrées doivent être booléen"
    return a or b

if __name__ =="__main__":
    pass
