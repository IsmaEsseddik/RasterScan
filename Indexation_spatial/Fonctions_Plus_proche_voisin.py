# coding: utf8
import random
import time
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def distance(point1, point2):
    """fonction qui retourne la distance entre les deux points en
    entrée de la fonction.
    :param point1: premier point
    :param point2: deuxieme point
    :return : distance entre le point 1 et 2
    """
    x1, y1, x2, y2=point1[0], point1[1], point2[0], point2[1] #recup x et y
    dist=((x2-x1)**2+(y2-y1)**2)**(1/2) #calcul de distance
    return dist

def point_aleatoire(xmin,ymin,xmax,ymax):
    """
    fonction retournant un point dont les coordonnÃ©es x et y sont
    tirés aléatoirement dans l'emprise ((xmin, ymin), (xmax, ymax)).

    :param xmin: abscisse minimale de l'emprise
    :param ymin: ordonnÃ©es minimale de l'emprise
    :param xmax: abscisses maximale de l'emprise
    :param ymax: ordonnÃ©es maximale de l'emprise
    :return : point au hasard
    """
    X=np.arange(xmin,xmax)
    Y=np.arange(ymin,ymax)
    xrand= random.choice(X)
    yrand= random.choice(Y)
    pointrand= (xrand,yrand)
    return pointrand

def points_aleatoires(n, xmin, ymin, xmax, ymax):
    """
    fonction retournant une liste de n points tirés aléatoirement.
    :param n: nombre de points a retourner
    :param xmin:abscisse minimale de l'emprise
    :param ymin:ordonnÃ©es minimale de l'emprise
    :param xmax:abscisses maximale de l'emprise
    :param ymax:ordonnÃ©es maximale de l'emprise
    :return : liste de points
    """
    liste=[]
    for i in range(0,n):
        liste.append(point_aleatoire(xmin,ymin,xmax,ymax))
    return liste    

#Approche naïve_________________________________________________

def plus_proche_voisin(p_ref, points):
    """
    fonction prenant en entrée un semis de n points tirés aléatoirement
    ainsi qu'un point référence (x, y).
    :param pref: point de refence.
    :param points: liste de points du semi.
    :return : liste contenent l'indice du point du semi
    le plus proche du point reference ainsi que la valeur de cette distance
    minimale.
    """
    #calcul de toutes distance entre p_ref et un point du semi
    #dans une liste Ldist
    n=len(points)
    Ldist=[]
    for i in range(n): #pour chaque point du semi, calcul et ajout de la distance
        Ldist.append(distance(p_ref, points[i]))
    if len(Ldist) == 0:
        print 'ne trouve pas de voisinage'
        return
    else:
        return [Ldist.index(min(Ldist)), min(Ldist)]

def temp_ppv(p_ref, points):
    """
    fonction retournant les temps de calculs pour un semi de points.(calcul de difference de temp entre fin et debut
    du processus).
    :param p_ref: point de reference.
    :param points: semi de point que l'on souhaite utiliser pour le calcul
    de temp.
    :return: la duree du calcul de la fonction.
    """
    temp_debut=time.time()
    plus_proche_voisin(p_ref, points)
    temp_fin =time.time()
    duree= temp_fin - temp_debut
    print duree
    return duree


def initindex(points, xmin, ymin, xmax, ymax, nlig, ncol):
    index = {'info ':{'xmin ': xmin, 'ymin ': ymin ,
                      'xmax ': xmax , 'ymax': ymax ,
                      'dx ': dx , 'dy ': dy ,
                      'nlig ': nlig , 'ncol ': ncol
                    }
             }
    for i in range(nlig):
        index[i]={}
        for j in range(ncol):
            index[i][j]=[]
    etx = np.arange(xmin, xmax)
    ety = np.arange(ymin, ymax)
    for pt in points:
        x, y = pt[0]-xmin, pt[1]-ymin
        ind = points.index(pt)
        if (x in etx and y in ety ):
            index[int(x/dx)][int(y/dy)].append(ind)
    return index        
            

def indice_index(point, xmin, ymin, dx, dy):
    """
    fonction retournant les indices de la cellule dans laquelle le
    point en entrÃ©e se situe.
    :param point: point d'entrÃ©e
    :param xmin: valeur abcisse minimale de la grille
    :param ymin: valeur ordonnÃ©es minimale de la grille
    :param dx: taille colonnes (xmin+ncol*dx=xmax)
    :param dy: taille des lignes (ymin+nlig*dy=ymax)
    :return : indices de la cellule dans laquelle se trouve le point
    dictionnaire.
    """
    etx = np.arange(xmin, xmax)
    ety = np.arange(ymin, ymax)
    x,y = point[0]-xmin, point[1]-ymin
    if (x in etx and y in ety ):
        return (int(x/dx),int(y/dy))
    else:
        print 'point out of bound'

def ppv_index(point_ref, points, indexes):
    list_pts=[]
    zone_id=indice_index(point_ref, xmin, ymin, dx, dy)
    col_zone=zone_id[0]
    lig_zone=zone_id[1]
    list_id_point = indexes[col_zone][lig_zone]
    if len(list_id_point) == 0:
        print "Zone vide ... -->"
        #si aucun pts dans la zone on creer les conditions a verifier pour l'ajout des zones voisine
        a = lig_zone != 0 # zone ailleur qu'en premiere ligne(peut on aller voir en haut?)
        b = col_zone != ncol-1 # ailleur qu'en derniere colone (peut on aller voir a droite?)
        c = lig_zone != nlig-1 # ailleur qu'en derniere ligne(peut on aller voir en bas?)
        d = col_zone != 0 # ailleur qu'en premiere colone (peut on aller voir a gauche?)
        if a:
            list_id_point += indexes[col_zone][lig_zone-1]
        if b :
            list_id_point += indexes[col_zone+1][lig_zone]
        if c :
            list_id_point += indexes[col_zone][lig_zone+1]
        if d :
            list_id_point += indexes[col_zone-1][lig_zone]
        if d and a :
            list_id_point += indexes[col_zone-1][lig_zone-1]
        if a and b :
            list_id_point += indexes[col_zone+1][lig_zone-1]
        if b and c :
            list_id_point += indexes[col_zone+1][lig_zone+1]
        if c and d :
            list_id_point += indexes[col_zone-1][lig_zone+1]
    for ids in list_id_point:
        list_pts.append(points[ids])
    return plus_proche_voisin(point_ref, list_pts)

def temp_ppv_index(point_ref, points, indexes):
    """
    Fonction retournant le temps de calcul pour un semi de points(calcul de difference de temp entre fin et debut
    du processus) du ppv avec index.
    :param p_ref: point de reference.
    :param points: semi de point que l'on souhaite utiliser pour le calcul
    de temp.
    :return: la duree du calcul de la fonction.
    """
    temp_debut=time.time()
    ppv_index(point_ref, points, indexes)
    temp_fin =time.time()
    duree= temp_fin - temp_debut
    print duree
    return duree


def time_graph(tailles, temps, temps_index=None):
    """
    fonction retournant un graphe representant la duree de calcul en fonction
    du nombre de point.
    :param taille: nombre de point d'un semi
    :param temps: temps de calcul pour le mÃªme semi
    :return: une fenetre avec graph (courbe,titre et axes libellÃ©).
    """
    #definition de la fonction
    plt.plot(taille, temps, color='red')
    legend = []
    red_patch = matplotlib.patches.Patch(color='red', label='Approche naive')
    legend.append(red_patch)
    if type(temps_index) == type([]) and len(temps_index) == len(taille):
        plt.plot(taille, temps_index, color='blue')
        blue_patch = matplotlib.patches.Patch(color='blue', label='Avec Indexation')
        legend.append(blue_patch)
        diff=[]
        for i in range(len(taille)):
            diff.append(temps[i]-temps_index[i])
        plt.plot(taille, diff, color='green')
        green_patch = matplotlib.patches.Patch(color='green',
                                               label='Gain de temps par Indexation')
        legend.append(green_patch)

    plt.title("Temps de calcul de la distance du plus proche voisin en fonction du nombre de points")
    #titre du graph
    plt.ylabel("Temps (s)")#libelÃ© abscisses
    plt.xlabel("Nombre de points") #libelé ordonnées
    plt.legend(handles=legend)
    plt.xscale('log')
    plt.show()# affichage de la courbe
    
#__test de fonction en ouverture_______________________________
if __name__ == '__main__':
    print '----------definition des parametres---------------'
    xmin = 0.
    ymin = 0.
    xmax = 20.
    ymax = 20.
    ncol = 5
    nlig = 5
    dx = (xmax-xmin)/ncol
    dy = (ymax-ymin)/nlig
    point = (10,10)
    print '----------generation des semis de points---------------'

    semi1 = points_aleatoires(10, xmin, ymin, xmax, ymax)
    semi2 = points_aleatoires(100, xmin, ymin, xmax, ymax)
    semi3 = points_aleatoires(1000, xmin, ymin, xmax, ymax)
    semi4 = points_aleatoires(10000, xmin, ymin, xmax, ymax)
    semi5 = points_aleatoires(100000, xmin, ymin, xmax, ymax)
    semi6 = points_aleatoires(1000000, xmin, ymin, xmax, ymax)

    print '----------generation des indexes---------------'
    index1=initindex(semi1,xmin,ymin,xmax,ymax,ncol,nlig)
    index2=initindex(semi2,xmin,ymin,xmax,ymax,ncol,nlig)
    index3=initindex(semi3,xmin,ymin,xmax,ymax,ncol,nlig)
    index4=initindex(semi4,xmin,ymin,xmax,ymax,ncol,nlig)
    index5=initindex(semi5,xmin,ymin,xmax,ymax,ncol,nlig)
    index6=initindex(semi6,xmin,ymin,xmax,ymax,ncol,nlig)
        
    # print plus_proche_voisin(point, semi3)
    # print ppv_index(point, semi3, indexes)
    # print temp_ppv(point,semi3)
    # print temp_ppv_index(point, semi3, indexes)

    taille = [10, 100, 1000, 10000, 100000, 1000000]
    temps = [temp_ppv(point, semi1),temp_ppv(point, semi2),
             temp_ppv(point, semi3),temp_ppv(point, semi4),
             temp_ppv(point, semi5),temp_ppv(point, semi6)]
    temps_index = [temp_ppv_index(point, semi1, index1),
                   temp_ppv_index(point, semi2, index2),
                   temp_ppv_index(point, semi3, index3),
                   temp_ppv_index(point, semi4, index4),
                   temp_ppv_index(point, semi5, index5),
                   temp_ppv_index(point, semi6, index6)]
    time_graph(taille, temps)
    time_graph(taille, temps, temps_index)
