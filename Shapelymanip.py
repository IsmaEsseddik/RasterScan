from shapely.geometry import Polygon
from shapely.wkt import loads
poly2 = Polygon([(1,2),(2,5),(6,5),(7,2),(5,1),(1,2)])
poly1 = loads(poly2.wkt)
point1 = loads('POINT (4 5)')
multipt = loads('MULTIPOINT ((2 2), (3 3), (3 4))')
ligne1 = loads('LINESTRING (3 1, 4 4, 5 5, 5 6)')
multiligne = loads('MULTILINESTRING ((1 2, 1 2, 2 1, 3 2),(2 4, 3 4, 5 3))')
ptbuf = point1.buffer(2)
linebuf = ligne1.buffer(2)
multiconvhull = multipt.convex_hull

if __name__=="__main__":
    print ("-----Debut-----")
    print 'les limites de ligne1 :',ligne1.bounds
    print 'la longueur de ligne1 :',ligne1.length
    print 'la zone du poly1 :',poly1.area

    print ("-----Fin-----")
