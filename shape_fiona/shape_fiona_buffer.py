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

def buffer_ptshp_to_geojson(nom_fichier, nom_sortie):
    """ Execute un buffer sur un shapefile """
    with fiona.open(nom_fichier, "r") as source:
        with open(nom_sortie+".geojson","w") as output:
            geojson = {"type": 'FeatureCollection', 'features': [], "crs":source.crs, "schema" : source.schema, "driver": source.driver}
            geojson['schema']['geometry'] = 'Polygon'
            cmpt=0
            for i in source:
                if i['geometry']['type'] == 'Point':
                    x,y= float(i['geometry']['coordinates'][0]), float(i['geometry']['coordinates'][1])
                    geom = Point(x, y).buffer(0.01)
                    ring = list(geom.boundary.coords) #on recupere le contour en tant que list de coordonnées
                    feat = { "type": "Feature", "geometry": {"type":"Polygon", "coordinates": [ring]}}
                    geojson['features'].append(feat)
                    geojson['features'][cmpt]['properties']=i['properties']
                cmpt+=1
            output.write(json.dumps(geojson, output, indent=4, sort_keys=True))
    print u"buffer exécuté"

def geojson_to_shp(nom_fichier, nom_sortie):
    """ Conversion d'un geojson en shapefile """
    with open(nom_fichier, "r") as source:
        geojson = json.load(source)
        print geojson['schema']
        with fiona.open(nom_sortie ,"w" ,driver = geojson['driver'], crs = geojson['crs'], schema = geojson['schema']) as output:
            for i in geojson['features']:
                for pt in i['geometry']['coordinates'][0]:
                    pt=tuple(pt)
                output.write(i)
        print u"shape créé"
    
if __name__=="__main__":
    lien ='gare_idf/gares-du-reseau-ferre-dile-de-france.shp'
    #buffer_ptshp_to_geojson(lien, 'garesbuffer')
    geojson_to_shp('garesbuffer.geojson','gare_buffer001')
