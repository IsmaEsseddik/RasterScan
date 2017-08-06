#-*- coding: utf-8 -*-
import numpy
import operator
import networkx as nx
import matplotlib.pyplot as plt

G = nx.read_graphml('metro.graphml') # lecture du graph
G = G.to_undirected() # ou to directe , pour un graph orienté ou non
def sommets_pendant(G):
    """retourne la liste des sommets pendant(ayant qu'un seule voisin)"""
    spd = []
    dg=nx.degree(G)
    for key, value in dg.iteritems():
        if value == 2:
            spd.append(key)            
    return spd

def degree_moyen(G):
    """retourne de la valeur du degree moyen"""
    deg = nx.degree(G) # dictionnaire le degré de chaque sommet
    list_deg = []
    for i in deg:
        list_deg.append(deg[i])
    return numpy.average(list_deg) #la moyenne de la liste

def degree_moyen2(G):
    listdeg = G.degree().values()
    return numpy.average(listdeg)

def vulnerable_list(G):
    """retourne la liste de la vulserabilité de chaque sommets.
    la vulnerabilité d'un sommet n dans un graph G est la difference entre
    le plus court chemin dans G et celui dans G sans le sommet n"""
    aspl = nx.average_shortest_path_length(G) # on calcul le chemin le plus court du graph G
    listvuln = []
    for n in G.nodes():
        try:
            G2= G.copy() # on fait une copie
            G2.remove_node(n) # en retirant le sommet n --> on a donc un sous graph G-n.
            aspl2 = nx.average_shortest_path_length(G2) # et on recalcul le chemin le plus court du sous graph G-n
            dif = aspl2-aspl # on fait la difference entre les deux resultat de calcul
            listvuln.append((dif,n)) #on stock le numero du noeud et sa vulnerabilité
        except nx.NetworkXError :
            print n
    print sorted(listvuln,reverse=True)

#pour le plus court chemin:
#nx.shortest_path(G, source='177 Lourmel', target='68 Parmentier')
#retourne la liste du cheminement des nom des sommet

"""
print 'ordre du graph ', nx.number_of_nodes(G) # ou G.order() , pour le nombre de  noeud alias l'ordre du graph
print "nombre d'arc ", nx.number_of_edges(G) # ou G.size() , pour le nombre de d'arc/aretes 
print "le graph est il connexe ",nx.is_connected(G) # pour savoir si le graph est connexe
for n in G.nodes(): #lister les noeuds
    print 'noeu ', n
print 'chemin le plus court ', nx.average_shortest_path_length(G) # moyenne
print 'voisinage de chatelet', G.neighbors('15 Chatelet') # fct simple
print 'voisinage2 de chatelet', [n for n in G.neighbors_iter('15 Chatelet')] # fct iterateur (consomme moins de données)

print sorted(deg, key=operator.itemgetter(1), reverse=True) # tri du dictionnaire

print nx.average_degree_connectivity(G)
print nx.average_neighbor_degree(G)
"""


nx.draw(G, nodelist=sommets_pendant(G))
plt.show()
