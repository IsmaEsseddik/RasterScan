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
class raster():
    tif = "3320D_2010_315_RGB_LATLNG.tif"
    
    def __init__(self):
        try:
            self.dataset = gdal.Open(str(self.tif), GA_ReadOnly)
        except RuntimeError, e: 
            print "Impossible d'ouvrir le fichier." 
            print e
            return
        self.meta = self.dataset.GetMetadata()
        self.cols = self.dataset.RasterXSize 
        self.rows = self.dataset.RasterYSize 
        self.bands = self.dataset.RasterCount
        self.driver = self.dataset.GetDriver()
        self.proj = self.dataset.GetProjection()
        self.gt = self.dataset.GetGeoTransform()
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
        self.tif = filename
        root.destroy()
        self.__init__()

    def valeurXY(self,bandek,x,y):
        band = self.dataset.GetRasterBand(bandek)
        return band.ReadAsArray()[y][x]

    def valeur_coordonnes(self,bandek,x,y):
        """fonction qui retourne la valeur du pixel aux coordonnées indiqué
        """
        band = self.dataset.GetRasterBand(bandek)
        xOffset = int((x - self.gt[0]) / self.gt[1])
        yOffset = int((y - self.gt[3]) / self.gt[5])
        data = band.ReadAsArray(xOffset, yOffset, 1, 1)
        return data[0,0]

            
    def profilelev(self,bandek,x_start,y_start,x_end,y_end,p):
        """fonction qui creer un un profil topo"""
        band = self.dataset.GetRasterBand(bandek)
        data = band.ReadAsArray()
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
        print ">-----------------------------METADONNEES-------------------------------<"
        if self.meta is not None:
            print self.meta
        print "Le raster est au format : ", self.driver.LongName
        print "_________________Projection, DATUM... _____ |WKT|____"
        print self.proj
        print "_____________________________________________________"
        print "il contient "+str(self.bands)+" bande(s), "+str(self.cols)+" colonnes, "+str(self.rows)+" lignes"
        print u"Coordonées a l'origine (x,y superieur gauche) : "+str(self.gt[0])+","+str(self.gt[3]) 
        print u"Résolution spatial Ouest-Est : "+str(self.gt[1])
        print u"Résolution spatial Nord-Sud : "+str(self.gt[5])
        print "Rotations : "+str(self.gt[2])+" , "+str(self.gt[4])
        print "Nombre de bandes : ", self.bands
        for i in range(1,self.bands+1):
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
        """Fonction qui retourne un scanline de l'emprise reechantillonné de
        la bande k specifié en argument"""#attention au raster trop grand
        band = self.dataset.GetRasterBand(bandek)
        bandtype = gdal.GetDataTypeName(band.DataType)
        scanline = band.ReadRaster(x0,y0,xn,yn,xs,ys,band.DataType)
        # coord x,y du pt de depart, ensuite taille (colonne,ligne) a recup dans le raster,
        # puis la taille du reechantillonnage enfin
        print scanline
        bt=''
        if bandtype == 'Byte':
            bt='b'
        elif bandtype == 'Float32':
            bt='f'
        else:
            return u"type de données non reconnu"
        values = struct.unpack(bt * xs * ys, scanline)
        return values

    def diagramdecimal(self,bandek):
        """Fonction qui represente les valeur de la bande k sous forme de
        diagramme.
        """
        band = self.dataset.GetRasterBand(bandek)  # bande passé en argument
        stats = band.GetStatistics( True, True ) # recuperation des données stat
        dataray = self.dataset.ReadAsArray()  # lecture en mode tableau
        fig, ax = plt.subplots(figsize=(16,8), subplot_kw={'projection': '3d'})  # definition du mode 3D
        xres = self.gt[1]  # resolution spatiale en x
        yres = self.gt[5]  # et en y
        zmin=stats[0]  # valeur min de Z
        zmax=stats[1]  # et max
        X = np.arange(self.gt[0], self.gt[0] + self.cols*xres, xres)  # delimitation le l'axe des x
        Y = np.arange(self.gt[3], self.gt[3] + self.rows*yres, yres)  # et des y
        X, Y = np.meshgrid(X, Y)  # definition d'une grille basé sur les axes x et y
        stride=10**(int(np.log10(self.cols)-1))  # pour le pas de la grille on prend le nb de colonnes generalement inferieur au nombre de ligne, divisé d'un facteur decimal 
        surf = ax.plot_surface(X,Y, dataray, rstride=stride, cstride=stride, cmap=plt.cm.RdYlBu_r, vmin=zmin, vmax=zmax, linewidth=0, antialiased=True)
        # definition des parametres de la grille(l'epaisseur, la coloration, le pas en colonne et en ligne.
        ax.set_zlim(zmin, zmax)  # limites de representation de z
        ax.view_init(60,-105)  # vue initiale
        fig.colorbar(surf, shrink=0.4, aspect=20)  # reglage de la legende couleur (longeur,minceur)
        ax.set_xlabel('X')  # etiquettes...
        ax.set_ylabel('Y')  # ...des...
        ax.set_zlabel('Z')  # ...axes
        plt.show()
        
    def subset(self,bandek,x0,y0,win_x=0,win_y=0):
        band = self.dataset.GetRasterBand(bandek)
        subset = band.ReadAsArray(x0, y0, win_x, win_y)
        return subset
        """
        driver = gdal.GetDriverByName('ENVI')
        driver.Register()
        outDataset = driver.Create('ENVI_subset', 50, 50, 1, gdal.GDT_Float32)
        http://geoinformaticstutorial.blogspot.fr/2012/10/creating-subset-of-raster-data-with.html
        """

    def w_rgb_addition(self,name):
        b, g, r = (self.dataset.GetRasterBand(k).ReadAsArray() for k in (1, 2, 3))
        total = np.zeros(r.shape) # creation d'un tableau de meme taille qu'une bande a valeur nuls(int32)
        for band in r, g, b:
            total += band
        total /= 3
        """
        # combinaison des bandes par addition, les valeurs depasseront certainement
        # la limite 8-bit integer, on a donc initialisé un tableau 64-bit float (type par defaut dans numpy)
        # l'ajout convertit donc les valeur et preserve le type float64bit.        
        profile = self.src.profile # màj des metadonnées pour les chgmts apportées=>creation d'un profile
        profile.update(dtype=rasterio.uint8, count=1, compress='lzw')  #(8bit,1 band, compression LZW)
        with rasterio.open(str(name)+'.tif', 'w', **profile) as dst:
            dst.write(total.astype(rasterio.uint8), 1) # ecriture du tableau
        """
        print total
                
    def histogram(self,bandek,classes):
        """Fonction qui affiche un histogramme represantent l'effectif de pixel)
        en fonction des valeurs en n classe"""
        band = self.dataset.GetRasterBand(bandek) # selection de la bande
        bandarray = band.ReadAsArray() #lecture de la bande
        stats = band.GetStatistics( True, True ) # recuperation des données stat
        vmin, vmax =stats[0], stats[1] # valeurs min&max
        plt.hist(bandarray,range=(vmin,vmax), bins=classes)
        plt.xlabel("valeurs")
        plt.ylabel("occurences")
        plt.title("Effectif de pixel en fonction des valeurs")
        plt.show()

    def standardisation(self,bandek,ligne,colone):
        """fonction qui standardise toute les valeurs du raster """
        band = self.dataset.GetRasterBand(bandek) # selection de la bande
        stats = band.GetStatistics( True, True ) # recuperation des données stat
        m = stats[2]  #moyenne
        std = stats[3]  #ecart-type
        lignes=[]
        bandarray = band.ReadAsArray() #lecture de la bande
        for i in range(0,ligne):
            colones=[]
            for j in range(0,colone):
                colones.append((bandarray[i][j]-m)/std)
            lignes.append(colones)
        return lignes


if __name__=="__main__":
    a = raster()
