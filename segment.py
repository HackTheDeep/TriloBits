from sys import argv
import cv2
import numpy as np
from matplotlib import pyplot as plt
import operator


# This file will take a "sufficiently" centered image of
# a well preserved trilobite and find areas of sharp change
# to find boundry points between parts of the trilobites body

# use "python segment.py [filename]"

# results on this are not 100% accurate but show that this
# might be the right path to a solution and should be expanded upon

# TODO:
# Come up with a metric to dynamically pick the window size to get
#		the best results
# Possiblity of passing over data a second time after peaks have
# 	Been found to eliminate false positives recognize patters to 
#		determine segments and differentation btwn head thorax and tail






# Helper function to use matplot lib with scanlines
def plot_graph(line, height, subcol, subrow, plotindex, color):
	i = 0
	prevx = 0
	prevy = 0
	plt.subplot(subcol,subrow,plotindex)
	for x in np.nditer(line):
		plt.plot([i,prevy], [x,prevx], color)
		plt.axis([0, height, 0, 255])
		prevx = x
		prevy = i
		i+=1	

# Draw original image with detected segments based on
# Scan Line derivative and window size
#		Input		#
# orignal image
# derivative of scanline
# window size
def find_local_max(img, line, window_size):
	height, width = img.shape
	start = 0
	end = window_size

	# get a local maxima within in a window
	# simple approach to find peaks in derivative
	for i in range(0,height,window_size):
		index, value = max(enumerate(line[start:end]), key=operator.itemgetter(1))
		img = cv2.line(img,(0,index+start),(width,index+start),(255,255,255))
		start += window_size
		end += window_size
	return img


def main():
	image_name = argv[1]

	# scale down image size
	img = cv2.pyrDown(cv2.pyrDown(cv2.imread(argv[1],0)))
	height, width = img.shape

	# get the center of the image
	middle = width/2
	middle = int(middle)

	# get a 1D scanline of the center of the image
	proc = img[0:height-1, middle:middle+1]

	blur = cv2.GaussianBlur(proc,(5,5),0)

	# compute first derivative of the scanline
	sobelx64f = cv2.Sobel(blur,cv2.CV_64F,0,1,ksize=1)
	# normalize values for representation
	abs_sobel64f = np.absolute(sobelx64f)
	sobel_8u = np.uint8(abs_sobel64f)
	# t = np.transpose(blur)

	#draw detected segements on image
	img = find_local_max(img, sobel_8u, 20)



	plot_graph(blur, height, 3, 1, 2 ,'k-')
	plot_graph(sobel_8u, height, 3, 1,2,'r-')

	cv2.imwrite('output.jpg',img)

	plt.show()

if __name__ == '__main__':
	main()