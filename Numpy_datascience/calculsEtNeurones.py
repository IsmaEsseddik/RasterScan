# coding: utf-8
import random
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
# -------------------------------------------------------------------------
"""

#-----------Systeme neuronale---------------------
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

class Neurone:
    """ Objet neurone artificiel a identifiant 'id' (entier positif). """
    # --------------------------- Constructeur ---------------------------
    def __init__(self,id):
        assert type(id) == 'int' and id>=0, "l'identifiant doit etre un entier positif"
        self.id = id

    # -------------------------- Somme ponderale des influx--------------------------------
    def somme_pond(self, X, W):
        """Calcule et retourne la valeur de la somme pondérale, """
        assert type(X) == type(W) == list, "les informations et poids doivent etre contenu dans des listes"
        assert len(X) == len(W), "les listes d'information et poids doivent etre de même taille"
        inf = 0
        for i in range(len(self.W)):
            assert type(X[i]) in ['int','float'] and 0<=X[i]<=1, "les informations doivent être reel et compris " \
                                                                 "entre 0 et 1, erreur : "str(i)
            assert type(W[i]) in ['int','float'], "les poids doivent etre de type numerique, erreur : "str(i)
            inf += self.X[i]*self.W[i]
        return inf

    # --------------- Fonctions g d'activation/transfert du neurone -------------
    def sigmoide(self,sp):
        y=1/(1+math.exp(-sp))
        return y

    def heaviside(self,sp):  # neurone a fonction lineaire et n entrées pondérées
        if (sp>=0):
            return 1
        else:
            return 0

    def sOUple(self,x1,x2):
        """ retourne un booleen sur un test logique OU avec seuil de signal (1/2)  """
        assert 0<=x1<=1 and 0<=x2<=1 ,"les deux entrées doivent être reel compris entre 0 et 1"
        if sp >= seuil:
            return 1
        else:
            return 0

    def XOR(self,x1,x2):
        """ retourne une valeur selon un test logique OU, """
        assert 0<=x1<=1 and 0<=x2<=1 ,"les deux entrées doivent être reel compris entre 0 et 1"
        if ((x1 ==1 and x2 != 1) or (x1 !=1 and x2 == 1) ):
            return 1
        else:
            return 0

def RdN(X, xWp, P ):
    """Reseaux de neurone avec X ndarray contenant les informations, xWp ndarray contenant les poids, P liste d'objects
    de classe neurone
    doit verifier que
    len(X) == len(matrice en ligne )
    len(P) == len(matrice en colone )
    matrice est de dtype numeric
    """

def matrex(n,p):
    inf = [-1]
    for i in range(n):
        inf.append(random.choice(range(1,10)))
    neurones = []
    for p in range(p):
        neurones.append(Neurone(np.ndarray())


if __name__ == "__main__":
    w=np.array([1,2,1,2,2,1,2])
    x=np.array([1,6,4,7,8,2,12],dtype=int)
    a = Neurone(x,w)
    x1 = 0.2
    x2 = 0.73
    x3 = 0
    x4 = 1
    print(fonction_XOR(x2, x2))
    print(fonction_XOR(x4, x2))
    matrex(5,6)



