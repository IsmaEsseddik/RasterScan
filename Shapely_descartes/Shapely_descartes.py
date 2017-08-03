# coding: utf8
from shapely.geometry import *
from shapely.wkt import loads
import pyproj
import json
import matplotlib.pyplot as plt
from descartes import PolygonPatch

# on cree un espace pour afficher un ou des graphiques :
fig = plt.figure(1, figsize=(7, 3), dpi=160)
# on definit un premier graph sur une grille a 1 ligne et 2 col en position 1
ax1 = fig.add_subplot(121)
# on definit un 2nd graph en position 2
ax2 = fig.add_subplot(122)

# on cree un ligne :
line = LineString([(0, 0), (1, 1), (0, 2), (2, 2), (3, 1), (1, 0)])
# on lui applique 2 buffers separement (=polygones)
dilated = line.buffer(0.5)
eroded = dilated.buffer(-0.3)
# d'autres polygones
poly = Polygon([(1,2),(2,5),(6,5),(7,2),(5,1),(1,2)])
multiligne = loads('MULTILINESTRING ((1 2, 1 2, 2 1, 3 2),(2 4, 3 4, 5 3))')    
dilated2 = multiligne.buffer(0.5)
# on rend les polygones compatible avec matplotlib
patch1 = PolygonPatch(dilated, fc='blue', ec='blue', alpha=0.5, zorder=2)
patch2 = PolygonPatch(eroded, fc='red', ec='red', alpha=0.5, zorder=2)
patch3 = PolygonPatch(poly, fc='green', ec='green', alpha=0.5, zorder=2)
patch4 = PolygonPatch(dilated2, fc='yellow', ec='yellow', alpha=0.5, zorder=2)
# on ajoute le polygone convertit sur le graph
ax1.add_patch(patch1)
ax1.add_patch(patch2)
ax2.add_patch(patch3)
ax2.add_patch(patch4)
# ajout des ligne source des buffer
ax1.plot(line.xy[0], line.xy[1], color='blue', linewidth=3, solid_capstyle='round', zorder=1)
for ligne in multiligne:
    ax2.plot(ligne.xy[0], ligne.xy[1], color='orange', linewidth=3, solid_capstyle='round', zorder=1)


# definition des axes x et y des graph 'ax1' et 'ax2'
ax1.axis([-2, 10, -2, 10])
ax2.axis([-2, 10, -2, 10])

#lister les ligne, pour chaque ligne : plot xy

plt.show()

def deuxrectingraph():
    fig = plt.figure()
    fig.gca().add_patch(plt.Rectangle((0, 1), 1, 1))
    fig.gca().add_patch(plt.Rectangle((3, 1), 1, 1))
    fig.gca().autoscale()
    plt.axis("equal")
    plt.show()

   
if __name__=="__main__":
    pass
"""
poly2 = loads(poly1.wkt) # well-known-text
point1 = loads('POINT (4 5)')
multipt = loads('MULTIPOINT ((2 2), (3 3), (3 4))')
ligne1 = loads('LINESTRING (3 1, 4 4, 5 5, 5 6)')
multiligne = loads('MULTILINESTRING ((1 2, 1 2, 2 1, 3 2),(2 4, 3 4, 5 3))')
ptbuf = point1.buffer(2)
linebuf = ligne1.buffer(2)
multiconvhull = multipt.convex_hull # envellope convexe
limites = ligne1.bounds
longueur = ligne1.length
zone = poly1.area
"""
