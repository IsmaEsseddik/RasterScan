# coding: utf8
import numpy as np  #ecriture de tableau en tuples de listes
import rasterio
import Tkinter as tk
import gdal
import tkFileDialog
gdal.UseExceptions()  # Pour permettre a gdal de faire usage des exception python

class Rasteriio:
    """usage de rasterio"""
    tif = "WhiteadderDEM.tif"
    def __init__(self):
        self.src= rasterio.open(self.tif)
        self.rdata = self.src.read()  # lecture du raster en tableau via numpy
        self.metadonnees()

    def openfile(self):
            root = tk.Tk()
            root.withdraw()
            root.overrideredirect(True)
            root.geometry('0x0+0+0')
            root.deiconify()
            root.lift()
            root.focus_force()
            self.tif = tkFileDialog.askopenfilename(parent=root)
            root.destroy()
            self.__init__()


    def w_rgb_addition(self,name):
        b, g, r = (self.src.read(k) for k in (1, 2, 3))
        total = np.zeros(r.shape) # creation d'un tableau de meme taille qu'une bande a valeur nuls(int32)
        for band in r, g, b:
            total += band
        total /= 3
        # combinaison des bandes par addition, les valeurs depasseront certainement
        # la limite 8-bit integer, on a donc initialisé un tableau 64-bit float (type par defaut dans numpy)
        # l'ajout convertit donc les valeur et preserve le type float64bit.        
        profile = self.src.profile # màj des metadonnées pour les chgmts apportées=>creation d'un profile
        profile.update(dtype=rasterio.uint8, count=1, compress='lzw')  #(8bit,1 band, compression LZW)
        with rasterio.open(str(name)+'.tif', 'w', **profile) as dst:
            dst.write(total.astype(rasterio.uint8), 1) # ecriture du tableu
    
    def metadonnees(self):
        print self.src.profile
            
if __name__ == "__main__": # https://github.com/mapbox/rasterio#dependencies
    a = Rasteriio()
        
