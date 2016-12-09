from osgeo import gdal
from scipy.spatial.distance import *
import sys

def getDistance(pixel_reflectance,material_reflectance):
	start=0
	end=len(material_reflectance)
	nm_val=0
	na_val=-1.23e34
	for reflectance in material_reflectance:
		if reflectance==nm_val or reflectance==na_val:
			start+=1
		else:
			break
	for i in range(len(material_reflectance)-1,-1):
		if material_reflectance[i]==nm_val or material_reflectance[i]==na_val:
			end-=1
		else:
			break

	pixel_reflectance=pixel_reflectance[start:end]
	material_reflectance=material_reflectance[start:end]

	d=sqeuclidean(pixel_reflectance,material_reflectance)*correlation(pixel_reflectance,material_reflectance)
	return d

def getMaterial(pixel_reflectance):
	global sig

	material='Unknown'
	material_class='Unknown'
	d={}

	for c in sig:
		d[c]={}
		for m in sig[c]:
			d[c][m]=getDistance(pixel_reflectance,sig[c][m])

	min_d=None
	for c in d:
		for m in d:
			if min_d==None or d[c][m]<min_d:
				min_d=d[c][m]
				material=m
				material_class=c

	return material,material_class

def segment(image,i,j):
	band_arrays=[]
	segmented_image={}

	for x in range(1,18):
		band=image.GetRasterBand(x)
		array=band.ReadAsArray()
		band_arrays.append(array[i:j])

	for row in range(i,j):
		for col in range(len(array[row])):
			pixel_reflectance=[]
			for band in range(1,18):
				pixel_reflectance.append(band_arrays[band][row][col])
			material, material_class=getMaterial(pixel_reflectance)
			segmented_image[(row,col)]=material_class

	return segmented_image

IMAGE_PATH='./Data/sundarbans_ISRO_data/IMS1_HYSI_GEO_114_05FEB2009_S1_TOA_REFLECTANCE_07_SPBIN.tif'
SIG_PATH='./processed_sig.p'

f=open('processed_sig.p','r')
sig=pickle.load(f)
f.close()

if len(sys.argv)!=3:
	print 'Usage: python segment.py <row_start> <row_end>'
else:
	i=int(sys.argv[1])
	j=int(sys.argv[2])
	image=gdal.Open(IMAGE_PATH,gdal.gdal.GA_ReadOnly)

	segmented_image=segment(image,i,j)

	f=open('output_'+str(i)+'_'+str(j)+'.p','w')
	pickle.dump(segmented_image,f)
	f.close()