# coding: utf8
from shapely.geometry import *
from shapely.wkt import loads
import pyproj
import fiona
from fiona.crs import *
import json

# WGS 84 = 4326 ; Web Mercator = 3857 ; Lambert-93 = 2154    

def metadatashp(shpfile):
    shape = fiona.open(shpfile, "r")
    print "crs : ", shape.crs
    print "schema : ", shape.schema
    print "driver : ", shape.driver
    print "number of feature : ", len(shape)
    shape.close()
    
def shptogeojson(shpfile,name_output):
    """fonction qui ecrit un fichier geojson a partir d'un fichier shape"""
    with open(name_output+".geojson","w") as output:
        shape = fiona.open(shpfile, "r")
        geojson = {"type": 'FeatureCollection', 'features': [], "crs":shape.crs, "schema" : shape.schema, "driver": shape.driver}
        for feature in shape:
            geojson['features'].append(feature)
        output.write(json.dumps(geojson, output, indent=4, sort_keys=True))

def reproj_shp(nom_fichier, nom_sortie, epsg2="2154"):
    """ Conversion des coordonnees d'un shapefile"""
    with fiona.open(nom_fichier, "r") as source:
        epsg1=str(source.crs['init'][5:])
        with fiona.open(nom_sortie ,"w" ,driver = source.driver, crs = from_epsg(epsg2), schema = source.schema) as output:
            for i in source:
                if (i['geometry']['type'] == 'Point'):
                    i['geometry']['coordinates'] = pyproj.transform(pyproj.Proj(init='EPSG:'+epsg1),
                                                                    pyproj.Proj(init='EPSG:'+epsg2),
                                                                    float(i['geometry']['coordinates'][0]),
                                                                    float(i['geometry']['coordinates'][1]))

                elif (i['geometry']['type'] == 'LineString' or i['geometry']['type'] == 'MultiPoint' ):
                    list_pt=[]      
                    for pt in i['geometry']['coordinates']:
                        pt = pyproj.transform(pyproj.Proj(init='epsg:'+epsg1),
                                           pyproj.Proj(init='epsg:'+epsg2),
                                           float(pt[0]), float(pt[1]))
                        list_pt.append(pt)
                    i['geometry']['coordinates'] = list_pt
                    
                elif (i['geometry']['type'] == 'Polygon' or i['geometry']['type'] == 'MultiLineString'):
                    list_ring = []
                    for ring in i['geometry']['coordinates']:
                        list_pt = []
                        for pt in ring:
                            pt = pyproj.transform(pyproj.Proj(init='epsg:'+epsg1),
                                                  pyproj.Proj(init='epsg:'+epsg2),
                                                  float(pt[0]), float(pt[1]))
                            list_pt.append(pt)
                        list_ring.append(list_pt)
                    i['geometry']['coordinates'] = list_ring
                            
                            
                elif (i['geometry']['type'] == 'MultiPolygon'):
                    list_poly = []
                    for poly in i['geometry']['coordinates']:
                        list_ring = []
                        for ring in poly:
                            list_pt = []
                            for pt in ring:
                                pt=pyproj.transform(pyproj.Proj(init='epsg:'+epsg1),
                                                   pyproj.Proj(init='epsg:'+epsg2),
                                                   float(pt[0]), float(pt[1]))
                                list_pt.append(pt)
                            list_ring.append(list_pt)
                        list_poly.append(list_ring)
                    i['geometry']['coordinates'] = list_poly
                    
                output.write(i)
        print u"shape reprojeté"
    
if __name__=="__main__":
    lien = "arrondissements/arrondissements.shp"
    lien2 = "essai.shp"
    lien3 = 'reprojL93_arrondissement/reprojL93_arrondissement.shp'
    lien4 = 'reprojL93_cap/reprojL93_cap.shp'
    #reproj_shp(lien,"reprojL93_arrondissement")
    #reproj_shp(lien2,"reprojL93_cap")
    #metadatashp(lien)
    #metadatashp(lien2)
    #metadatashp(lien3)
    #metadatashp(lien4)
    shape_in_graph()
