import sys
import pickle
from PIL import Image

def draw(segmented_image, color_pallete):

	i=None
	j=None
	col_length=None
	for pixel in segmented_image:
		if i==None:
			i=pixel[0]
			j=pixel[0]
		else:
			i=min(pixel[0],i)
			j=max(pixel[0],j)
		if col_length==None:
			col_length=pixel[1]
		else:
			col_length=max(pixel[1],col_length)

	size=(j-i,col_length)
	mode='RGB'

	image=Image.new(mode,size)
	for pixel in segmented_image:
		image.putpixel((pixel[0]-i,pixel[1]),color_pallete[segmented_image[pixel]])

	image.save('output_'+str(i)+'_'+str(j)+'.jpeg')


if len(sys.argv)!=2:
	print 'Usage: python visualize.py <output_file>'
else:
	f=open(sys.argv[1],'r')
	segmented_image=pickle.load(f)
	f.close()

	color_pallete={
		'Unknown':(0,0,0),
		'A':(200,200,200),
		'C':(255,0,255),
		'L':(0,0,255)
		'M':(255,255,0)
		'S':(255,0,0)
		'V':(0,255,0)
	}

draw(segmented_image, color_pallete)

