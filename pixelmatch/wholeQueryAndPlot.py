import matplotlib
matplotlib.use('Agg')
import spectral.io.envi as envi
import pickle
import r2r
import math
import Image
import sys
import matplotlib.pyplot as plt
from PIL import Image

def d(X,Y):
        d = (X - Y) ** 2
        return d

def d_min(ref, wavelength):
        wavelength /= 1000
        minD = None
        minTuple = ()
        na_val = -1.23e+34
        nm_val = 0
        for t in ref:
                #ignore the tuple if reflectance not valid
                if t[1] == na_val or t[1] == nm_val:
                        continue
                dist = d(t[0], wavelength)
                if minD == None or dist < minD:
                        minD = dist
                        minTuple = t
        #print "wavelength: ",wavelength," minTuple: ",minTuple,"\n"
        return minTuple[1]

def neighbours(ref, band_centers):
#find the vector of reflectance for nearest wavelengths corresponding to the band centers
        v = []
        for i in band_centers:
                v.append(d_min(ref,i))
        return v
        
def sqerror(pixel_reflectance, NN_reflectance):
        err = 0
        na_val = -1.23e+34
        nm_val = 0
        for i in range(len(pixel_reflectance)):
                if pixel_reflectance[i] == na_val or pixel_reflectance[i] == nm_val:
                        continue
                err += (pixel_reflectance[i] - NN_reflectance[i]) ** 2 / (pixel_reflectance[i] ** 2 * NN_reflectance[i] ** 2)
        return err


f = open('../sig.p','r')
sig = pickle.load(f)
f.close()

name=r'EO1H1380452014327110KZ.L1R'
hdr=r'EO1H1380452014327110KZ.hdr'
img=envi.open(hdr,name)
centers = img.bands.centers
meta = (centers,327,0)
shape = img.shape
for c in sig:
        hist_arr = []
        print "class: ",c
        for t in sig[c]:
                print "material: ",t
                v = neighbours(sig[c][t], centers)      #v is the vector of nearest neighbouring wavelengths for the material t in sig[c]
                err_arr = []
                for i in range(shape[0]):
#                       print "i= ",i
                        for j in range(shape[1]):
#                               print "j= ",j
                                pixel_reflectance = r2r.reflectanceVector(img.read_pixel(i,j),meta)
                                err_arr.append(sqerror(pixel_reflectance,v))
                hist_arr.append(min(err_arr))
        n,bins,patches = plt.hist(hist_arr, 50)
        plt.xlabel("min. sq. error")
        plt.yabel("Frequency")
        plt.grid(True)
        plt.savefig("Material_"+c+".jpeg")
