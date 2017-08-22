# coding: utf8
import numpy as np

# __________creation de matrice numpy___________
# le type de donnée dtype peut etre int , float bool etc.
# mais avec numpy on peut avoir d'autre format du langage C

np.zeros(10, dtype=int)
#cree une matrice a une dimension de 10 valeur nul de meme type entier
np.ones((3, 5), dtype=float)
# une matrice de dimension 3x5 de valeurs flottantes de 1
np.full((3, 5), 3.14)
# une matrice 3x5 pleine de valeur 3.14
np.arange(0, 20, 2)
# start, stop, step
np.linspace(0, 1, 5)
# start , stop, nombre de valeurs
#---->discretiation de l'etendu [0:1] en 4 classes d'amplitude egales
np.random.random((3, 3))
#matrice 3x3 de valeurs aleatoire entre 0et1 dont la distribution statistique est uniforme
np.random.normal(0, 1, (3, 3))
# matrice 3x3 de valeurs aleatoire dont la distribution stat est normalisé
# avec une moyenne de 0 et un ecart-type de 1
np.random.randint(0, 10, (3, 3))
# matrice 3x3 de aleatoire entiers  dans l'intervale 0 à 10
np.eye(3)
# matrice identité 3x3(matrice carré avec 1 sur toute la diagonal et 0 partout ailleurs
np.empty(3)
# cree une matrice non intialisé de 3 entiers

#____________ Attributs de matrice_________________
np.random.seed(0)  # (ré)initialisation generateur de valeurs aleatoires
x1 = np.random.randint(10, size=6)  # matrice a 1 dimension de valeur aleatoire(6valeur entre 0,10)
x2 = np.random.randint(10, size=(3, 4))  # matrice 2D 
x3 = np.random.randint(10, size=(3, 4, 5))  # 3D
x3.ndim # nb de dimension
x3.shape # forme de la matrice : tuple donnant la taille de chaque dimension 
x3.size # taille de la matrice : nb de cellule
x3.dtype # type de donnée de la matrice
x3.itemsize # taille d'une cellule en octets
x3.nbytes # size*item size = taille de la matrice en octets

#____________ Acces aux cellules_________________
#matrice[d1=start:stop:step,d2,d3,etc]
x4=x3[3:8:2,:8:3,6:2:-1].copy() #pour faire un copy de la matrice
x1.reshape((6,1))# pour changer la forme de la matrice en conservant les valeurs
x1[:,,]# on peut aussi faire ajouter un axe dans la referenciation de cellule


#____________Concatenation et seperation de matrice_________________
np.concatenate([x1, x1]) # on peut concatener des matrice de meme dimensions uniquement
np.concatenate([x1,x2,x3],axis=0) # on peut ajouter l'argument axis pour l'empilement selon une dimension/axe: penser jeu de carte
np.vstack([x, grid]) # on utilise la fct stack (vertical, horiz ou d) pour les empiler 
# il ne peut y avoir de nb d'elements different sur chaque list/plan d'un meme plan/volume
np.split(x,(2,4))# split divise la sequence en des points de separation
#hsplit divise les matrice horizontalement, vplit verticalement, dsplit dans le 3iem axe


if __name__ == "__main__":
    pass
