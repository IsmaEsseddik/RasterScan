# coding: utf8
import struct  # pour interpreter les chaines de caractere en donnée binaires compressé.
from mpl_toolkits.mplot3d import Axes3D
from osgeo import gdal, gdalnumeric, ogr, osr
import os, sys
gdal.UseExceptions()  # Pour permettre a gdal de faire usage des exception python
from gdalconst import * 
from shapely.geometry import * 
import numpy as np  # calculs numerique
from matplotlib import pyplot as plt  # graph.
from matplotlib.mlab import griddata
from matplotlib import cm
import Tkinter as tk
import tkFileDialog
import sys
#------------------------------------------------------------------------------
line1 = LineString([(0, 0), (5, 4)])  # creation d'un objet ligne 
line2 = LineString([(5, 0), (0, 4)])
tif = "C:\Users\isma\Desktop\Python\WhiteadderDEM.tif"
dataset = None
MNT=[[0,0,1,1,0],[0,1,2,2,1],[1,2,2,1,0],[2,3,2,2,1],[3,4,3,2,1],[2,3,2,1,0]]


class raster():
    tif = "C:\Users\isma\Desktop\Python\WhiteadderDEM.tif"
    
    def __init__(self):
        #tif = self.openfile()
        try:
            self.dataset = gdal.Open(self.tif, GA_ReadOnly)
        except RuntimeError, e: 
            print "Impossible d'ouvrir le fichier." 
            print e
            return
        self.metadonnees()

    def openfile(self):
        root = tk.Tk()
        root.withdraw()
        root.overrideredirect(True)
        root.geometry('0x0+0+0')
        root.deiconify()
        root.lift()
        root.focus_force()
        filename = tkFileDialog.askopenfilename(parent=root)
        print filename
        root.destroy()

    def valeurXY(self,x,y):
        return self.dataset.ReadAsArray()[y][x]
            
    def profilelev(self,x1,y1,x2,y2,p):
        """fonction qui creer un un profil topo"""
        data = self.dataset.ReadAsArray()
        if x1>data.shape[1]  or x2>data.shape[1] or y1>data.shape[0] or y2>data.shape[0]:  # on verifie que les valeurs sont bien interne au raster
            return 'erreur : le profil est OOB, dimensions : ', data.shape[1], data.shape[0]
        ligne = LineString([(x1,y1),(x2,y2)])
        lon = ligne.length  # longueur de la ligne
        dist=[]  # pour stocker le couple distance
        h=[]  # pour stocker l'altitude
        for i in np.arange(0,int(lon),p):  # on creer une boucle sur la longueure 
            dist.append(i)  # on ajoute la distance
            point=ligne.interpolate(i).coords[:]  # on recupere la position sur le raster par rapport a la distance
            x=point[0][0]
            y=point[0][1]
            h.append(data[int(y)][int(x)])  # row puis col
        plt.plot(dist, h)
        plt.show()

    def polygoniser(self, bandek, nom):
        """Fonction qui creer un shapefile a partir du raster, toutes les zones
        conectées partageant une valeur pixellaire commune seront polygonisé.
        ces polygones on une ID mais rien d'autre
        """
        try:  # ouverture de la band i
            srcband = self.dataset.GetRasterBand(bandek)
        except RuntimeError, e:
            # for example, try GetRasterBand(10)
            print "La bande "+str(bandek)+" n'existe pas"
            print e
            return
        drv = ogr.GetDriverByName("ESRI Shapefile")
        dst_ds = drv.CreateDataSource(nom+".shp" )
        dst_layer = dst_ds.CreateLayer(nom, srs = None )
        gdal.Polygonize(srcband, None, dst_layer, -1, [], callback=None)

    def metadonnees(self): 
        meta = self.dataset.GetMetadata()
        cols = self.dataset.RasterXSize 
        rows = self.dataset.RasterYSize 
        bands = self.dataset.RasterCount
        driver = self.dataset.GetDriver()
        proj = self.dataset.GetProjection()
        geotransform = self.dataset.GetGeoTransform()
        print ">-----------------------------METADONNEES-------------------------------<" 
        print u'Unité de resolution(1=sans unite 2=inch 3=cm):', meta['TIFFTAG_RESOLUTIONUNIT']
        print u'Résolution en x:', meta['TIFFTAG_XRESOLUTION']
        print u'Résolution en y:', meta['TIFFTAG_YRESOLUTION']
        print '_________________Source logiciel_________________ :\n', meta['TIFFTAG_SOFTWARE'] 
        print "Le raster est au format : ", driver.LongName
        print "_________________Projection, DATUM... _____ |WKT|____"
        print proj
        print "_____________________________________________________"
        print "il contient "+str(bands)+" bande(s), "+str(cols)+" colonnes, "+str(rows)+" lignes"
        print u"Coordonées a l'origine (x,y superieur gauche) : "+str(geotransform[0])+","+str(geotransform[3]) 
        print u"Résolution spatial Ouest-Est : "+str(geotransform[1])
        print u"Résolution spatial Nord-Sud : "+str(geotransform[5])
        print "Rotations : "+str(geotransform[2])+" , "+str(geotransform[4])
        print "Nombre de bandes : ", bands
        for i in range(1,bands+1):
            print u"---------------> BANDE N°"+str(i)
            band = self.dataset.GetRasterBand(i)
            if band is None:
                print u"xxxx-Pas de données-xxxx"
                continue
            bandtype = gdal.GetDataTypeName(band.DataType)
            print u"[TYPE DE DONNEES] : '"+bandtype+"'"
            print "[ DIMENSIONS ] (x,y) :", band.XSize, ",", band.YSize
            print "[ STATS ] :"
            stats = band.GetStatistics( True, True )
            if stats is not None:
                print'Min=',stats[0]
                print'Max=',stats[1]
                print'Moyenne=', stats[2]
                print'Ecart-type=', stats[3]
            print "[ NO DATA VALUE ] : ", band.GetNoDataValue()
            print "[ ECHELLE ] : ", band.GetScale()
            print "[ TYPE D'UNITE ] : ", band.GetUnitType()
            print "[ COLORTABLE ] : "
            ctbl=band.GetColorTable()
            if ctbl is not None:
                print " [ COLOR TABLE COUNT ] : ", ctable.GetCount()
                for i in range( 0, ctable.GetCount() ):
                    entree = ctable.GetColorEntry( i )
                    if not entree:
                        continue
                    print "[ COLOR ENTRY RGB ] = ", ctable.GetColorEntryAsRGB( i, entry )
            print">-----------------------------------------------------------------------<"
                    
    def getScanline(self,bandek,x0,y0,xn,yn,xs,ys):
        band = self.dataset.GetRasterBand(bandek)
        scanline = band.ReadRaster(x0,y0,xn,yn,xs,ys,band.DataType)
        # coord x,y du pt de depart, ensuite taille (colonne,ligne) a recup dans le raster,
        # puis la taille du reechantillonnage enfin
        print scanline
        values = struct.unpack('f' * xs * ys, scanline)
        return values

    def diagramdecimal(self,bandek):
        gt = self.dataset.GetGeoTransform() # données de projection
        cols=self.dataset.RasterXSize  # nb de colones
        rows=self.dataset.RasterYSize  # nb de lignes
        band = self.dataset.GetRasterBand(bandek)  # bande passé en argument
        stats = band.GetStatistics( True, True )  # données statistiques
        dataray = self.dataset.ReadAsArray()  # lecture en mode tableau
        fig, ax = plt.subplots(figsize=(16,8), subplot_kw={'projection': '3d'})  # definition du mode 3D
        xres = gt[1]  # resolution spatiale en x
        yres = gt[5]  # et en y
        zmin=stats[0]  # valeur min de Z
        zmax=stats[1]  # et max
        X = np.arange(gt[0], gt[0] + cols*xres, xres)  # delimitation le l'axe des x
        Y = np.arange(gt[3], gt[3] + rows*yres, yres)  # et des y
        X, Y = np.meshgrid(X, Y)  # definition d'une grille basé sur les axes x et y
        stride=10**(int(np.log10(cols)-1))  # pour le pas de la grille on prend le nb de colonnes generalement inferieur au nombre de ligne, divisé d'un facteur decimal 
        surf = ax.plot_surface(X,Y, dataray, rstride=stride, cstride=stride, cmap=plt.cm.RdYlBu_r, vmin=zmin, vmax=zmax, linewidth=0, antialiased=True)
        # definition des parametres de la grille(l'epaisseur, la coloration, le pas en colonne et en ligne.
        ax.set_zlim(zmin, zmax)  # limites de representation de z
        ax.view_init(60,-105)  # vue initiale
        fig.colorbar(surf, shrink=0.4, aspect=20)  # reglage de la legende couleur (longeur,minceur)
        ax.set_xlabel('X')  # etiquettes...
        ax.set_ylabel('Y')  # ...des...
        ax.set_zlabel('Z')  # ...axes
        plt.show()

    def histogram(self,bandek,classes):
        band = self.dataset.GetRasterBand(bandek) # selection de la bande
        bandarray = band.ReadAsArray() #lecture de la bande
        stats = band.GetStatistics( True, True ) # recuperation des données stat
        vmin, vmax =stats[0], stats[1] # valeurs min&max
        plt.hist(bandarray,range=(vmin,vmax), bins=classes)
        plt.xlabel("valeurs")
        plt.ylabel("occurences")
        plt.title("Effectif de pixel en fonction des valeurs")
        plt.show()

if __name__=="__main__":
    # metadonneestif(tif)
    # print getScan1stline(tif,1)
    # print getValue(tif,1,60,70)
    # 486 , 645
    a=raster()
