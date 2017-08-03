# coding: utf8
from shapely.geometry import *
from shapely.wkt import loads
from gdal import *
import pyproj
import fiona
import json
import networkx
import csv
# WGS 84 = 4326 ; Web Mercator = 3857 ; Lambert-93 = 2154

def readlinescsv(lien):
    contenucsv=[] #pour lister chaque ligne du csv (liste de liste
    with open(lien, 'r') as csvfile:
        lecture = csv.reader(csvfile, delimiter=",")
        for row in lecture:
            contenucsv.append(row)
        contenucsv.pop(0) # On retire les en-tete
        return contenucsv

def array_to_geojson(array):
    jsondico = {"type":"FeatureCollection", "features":[],"crs":'NULL', "schema" : 'NULL', "driver": 'NULL'}
    for entry in array:
        lat=float(entry[0])
        lon=float(entry[1])
        geometry= {"type":"Point", "coordinates":[lon,lat]}
        city=entry[2]
        properties= {"nom_ville":city}
        feature={"type":"Feature","geometry":geometry, "properties": properties}
        jsondico["features"].append(feature)
    return jsondico

def compact_geojson(dico):
    """convertit en str"""
    return json.dumps(dico, separators=(',',':'))

def pretty_geojson(dico):
    """convertit en str avec indentation"""
    return json.dumps(dico, sort_keys=True, indent=4, separators=(',', ': '))

def ecriture_geojson(dico, nom_fichier):
    with open(nom_fichier, 'w') as outfile:
        outfile.write(json.dumps(dico, outfile, indent=4, sort_keys=True))

def reproj_geojson(nom_fichier, epsg1="4326", epsg2="3857"):
    """ Conversion des coordonnees d'un geojson"""
    with open(nom_fichier, 'r') as file:
        lecture = file.read()
        geojson = json.loads(lecture)
        for i in geojson['features']:
            if (i['geometry']['type'] == 'Point'):
                e=pyproj.transform(pyproj.Proj(init='epsg:'+epsg1), pyproj.Proj(init='epsg:'+epsg2),float(i['geometry']['coordinates'][0]), float(i['geometry']['coordinates'][1]))
                i['geometry']['coordinates'][0] = e[0]
                i['geometry']['coordinates'][1] = e[1]
    #verifier avec qgis
    ecriture_geojson(geojson, 'proj_to'+epsg2+'_'+nom_fichier)
    print u"fichier reprojeté"
    
if __name__=="__main__":
    lien = "villes_importantes.csv"
    array = readlinescsv(lien)
    jsondico = array_to_geojson(array) 
    ecriture_geojson(jsondico,'test.geojson')
    reproj_geojson('test.geojson')
    


