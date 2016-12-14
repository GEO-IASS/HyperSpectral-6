import spectral.io.envi as envi
import pickle
import r2r
import math
import Image
import sys
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
		if t[0] == na_val or t[0] == nm_val:
			continue
		#(TODO):ignore reflectance?
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

def classify(testpixel, reflectance):
#normalized sum of squares <= 0.5 (TODO): proper thresholding
	error = 0
	valid_pts = 0
	na_val = -1.23e+34 
	nm_val = 0
	for i in range(len(reflectance)):
		if testpixel[i] == na_val or testpixel[i] == nm_val:
			continue
		valid_pts += 1
	#	print "testpixel: ",testpixel[i]," reference: ",reflectance[i],"\n"
		error += (testpixel[i] - reflectance[i]) ** 2
	return (error/valid_pts)
	'''
	print "valid_pts= ",valid_pts,"\n"
	error /= valid_pts 	
	print "error: ",error
	if error <= 0.5:
		return True
	else:
		return False	
	'''

def compare(row_start, row_end, _type, material, sig, band_centers):
	name = None
	for t in sig[_type]:
		if (t == material):
			name = material
			v = neighbours(sig[_type][t], band_centers)
	
	if name == None:
		print "Invalid material name"
		return

	errimg = [[0 for x in range(shape[1])] for y in range(shape[0])]	
	image = Image.new('RGB',(shape[0],shape[1]))
	for i in range(shape[0]):
		for j in range(shape[1]):
			pixel_reflectance = r2r.reflectanceVector(img.read_pixel(i,j),meta)
			error = classify(pixel_reflectance, v)
			errimg[i][j] = error

	print errimg
	return

	'''
	image = Image.new('RGB',(row_end - row_start + 1, shape[1]))

	
	for i in range(row_start, row_end + 1):
		for j in range(shape[1]):
			pixel_reflectance = r2r.reflectanceVector(img.read_pixel(i,j),meta) #r2r(img[i,j])
			truth = classify(pixel_reflectance, v)		#####(TODO):color according to classification
			if truth:
				image.putpixel((i-row_start,j),(255,255,0))
			else:
				image.putpixel((i-row_start,j),(255,0,0))
	#image.save('pixelwiseclassificationoutputfor'+material+'_row'+str(row_start)+' - row'+str(row_end)+'.jpeg')	
				
	return
	'''

if len(sys.argv) != 3:
	print "format: python <filename> <start_row> <end_row>"
else:
	row_start=int(sys.argv[1])
	row_end=int(sys.argv[2])
	print "Type of Material:"
	while True:
		print "1. Artificial (Man Made) Including Manufactured Chemicals\n2. Liquids, Liquid Mixtures, Water, and Other Volatiles Including Frozen Volatiles\n3. Minerals\n4. Soils, Rocks, Mixtures,and Coatings\n5. Plants, Vegetation Communities, and Mixtures with Vegetation\n6. Others"
		typeOfMaterial = raw_input()
		if typeOfMaterial == "1":
        		#take the appropriate material's data and scan	
        		_type = "A - Artificial"
        		break
		elif typeOfMaterial == "2":
        		_type = "L - Liquids"
			break
        	elif typeOfMaterial == "3":
        		_type = "M - Minerals"
			break
        	elif typeOfMaterial == "4":
        		_type = "S - Soils"
			break
        	elif typeOfMaterial == "5":
        		_type = "V - Vegetation"
			break
        	elif typeOfMaterial == "6":
        		_type = "C"
			break
        	else:
        		print "Choose from 1 - 6"


	print "Material name:"
	material = raw_input()
	print row_start," , ",row_end," , ",typeOfMaterial," , ",material
	print 'Classifying rows:',row_start,'-',row_end
	name=r'EO1H1380452014327110KZ.L1R'
	hdr=r'EO1H1380452014327110KZ.hdr'
	img=envi.open(hdr,name)
	shape = img.shape
	centers = img.bands.centers
	meta=(centers,327,0)
	print img

	f = open('sig.p','r')
	sig = pickle.load(f)
	f.close()

	compare(row_start, row_end, _type, material, sig, centers)
