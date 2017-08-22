# coding: utf-8

# Ce script est l'application theorique des elements en provenance de cet page:
# http://alp.developpez.com/tutoriels/intelligence-artificielle/reseaux-de-neurones/

# import random
import math
import numpy as np
# import matplotlib as plt
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

# -----------Système neuronale---------------------
class Neurone:
    """ Objet neurone artificiel doté d'un identifiant 'id' (entier positif). """
    # --------------------------- Constructeur ---------------------------
    def __init__(self, identifiant):
        assert type(identifiant) is int and identifiant >= 0, "l'identifiant doit etre un entier positif"
        self.id = identifiant

    # -------------------------- Somme ponderale des influx--------------------------------
    def somme_pond(self, X, W):
        """Calcule et retourne la valeur de la somme pondérale, """
        assert type(X) == type(W) == list, "les informations et poids doivent etre contenu dans des listes"
        assert len(X) == len(W), "les listes d'information et poids doivent etre de même taille"
        inf = 0
        for i in range(len(W)):
            assert type(X[i]) in [int, float] and 0<=X[i]<=1, "les informations doivent être reel et compris " \
                                                                 "entre 0 et 1, erreur : "+str(i)
            assert type(W[i]) in [int, float], "les poids doivent etre de type numerique, erreur : "+str(i)
            inf += X[i]*W[i]
        return inf

    # --------------- Fonctions g d'activation/transfert du neurone -------------
    def sigmoide(self, X, W):
        sp=self.somme_pond(X, W)
        y=1/(1+math.exp(-sp))
        return y

    def heaviside(self, X, W):  # neurone a fonction lineaire et n entrées pondérées
        sp=self.somme_pond(X,W)
        if (sp>=0):
            return 1
        else:
            return 0

    def sOUple(self, x1, x2):
        """ retourne un booleen sur un test logique OU avec seuil de signal (1/2)  """
        assert 0<=x1<=1 and 0<=x2<=1 ,"les deux entrées doivent être reel compris entre 0 et 1"
        if x1+x2 >= 0.5:
            return 1
        else:
            return 0

    def neurxor(self, x_1, x_2):
        """ retourne une valeur selon un test logique OU, """
        assert 0<=x_1<=1 and 0<=x_2<=1 ,"les deux entrées doivent être reel compris entre 0 et 1"
        if ((x_1 ==1 and x_2 != 1) or (x_1 !=1 and x_2 == 1) ):
            return 1
        else:
            return 0

    # -----------------------Apprentissage par descente de gradient---------------------------
    def quadratic_error(self, y, yd, alpha=0.5):
        """retourne l'erreur quadratique (la moitié du carré de la difference entre theorie et pratique)avec
        :y: resultat de la empirique
        :yd: yd resultat theorique
        """
        return (math.sqrt(y-yd)) / 2

    """
    def dwnlearn_grad(self,XYk,W,alpha=0.5):
        Fonction qui retourne la liste des n poids modifié,avec
        :XYk: une liste de N exemples (tuple k) possedant une liste d'informations et le resultat attendu.
        :W: liste des n poids actuels
        dw=[] #on creer une liste de poids
        print(dw)
        for i in range(0,len(w)): # on les initialise tous a 0
            dw[i]=0
        for e in XYk: # pour chaque exemple
            sk=self.sigmoide(e[0],W) #calcul du resultat sk avec les poids actuels
            for i in dw:
                dw[i]+= alpha*(e[1]-sk)*e[0][i]
        print(dw)
        for i in dw:
            W[i]+=i
        # Fonction non testé
    """

    def learn_Widrow_Hoff(self, XYk, W, alpha=0.5):
        """Fonction qui retourne la liste des n poids modifié, avec
        :XYk: une liste de N exemples (tuple k) possedant une liste d'informations et le resultat attendu.
        :W: liste des n poids actuels
        """
        for e in XYk: # pour chaque exemple
            sk=self.sigmoide(e[0],W) #calcul du resultat sk avec les poids actuels
            for i in W:
                i+= alpha*(e[1]-sk)*e[0][i]
        return W  # a essayer


class Perceptron:
    """ Réseau de neurones monocouche"""
    def __init__(self,nb,mode='ff'):
        """Constructeur de perceptron, prend en entrée un nombre de neurone ansi que le type
        'feed-forward'(normaux) ou 'récurrents'(alimentent leurs entrées avec leurs sorties)"""
        assert type(nb) is int and nb>0, 'nb doit etre entier positif'
        self.rdn = []
        for i in range(nb):  # on va creer une liste de 5 objets de la class neurones, identifié par un numero de 0a4
            self.rdn.append(Neurone(i))

    def rdn_activ(self,X, M):
        """Fonction d'activation du reseaux de neurone, avec
        :X: liste d'informations,
        :M: matrice 'ndarray' contenant les poids info/neurone,
        """
        assert type(M) is np.ndarray and M.ndim == 2, "ce n'est pas une matrice 'ndarray' en 2 dimension"
        assert np.issubdtype(M.dtype, np.number), "La matrice n'est pas integralement de type numerique ?"
        assert len(X) == len(M), "le nombre d'information ne correspond pas a la matrice"
        assert len(self.rdn) == len(M[0])
        list_activ = []
        for neu in self.rdn:
            W = []
            for i in range(len(X)):
                W.append(int(M[i][neu.id]))
            list_activ.append(neu.heaviside(X, W))
        return list_activ

if __name__ == "__main__":
    W = [1,2,1,2,2,1,2]
    X = [0.1,0.6,0.4,0.7,0.8,0.2,0.12]
    a = Neurone(0)
    x1, x2, x3, x4 = 0.2, 0.73, 0, 1
    print(a.neurxor(x2, x2))
    print(a.sOUple(x4, x2))
    print(a.heaviside(X,W))
    print(a.sigmoide(X,W))
    P=Perceptron(5)
    M = np.random.randint(-2, 4, ((len(X), len(P.rdn))))  # Creation d'une matrice de ponderation neuroneXinfo aleatoire
    print(M, type(M))
    print(P.rdn_activ(X,M))
