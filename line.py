import numpy as np
import cv2
from matplotlib import pyplot as plt

def auto_canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)
 
	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
 
	# return the edged image
	return edged




def thresh_callback(thresh, blur, img):
    # edges = cv2.Canny(blur,thresh,thresh*2)
    # wide = cv2.Canny(blurred, 10, 200)
    edges = cv2.Canny(blur, 200, 250)
    minLineLength = 0
    maxLineGap = 0
    lines = cv2.HoughLines(edges,1,np.pi/180, 16)

    for line in lines:
      for r,theta in line:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*r
        y0 = b*r
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        cv2.line(img,(x1,y1), (x2,y2), (0,0,255),2)
    # drawing = np.zeros(img.shape,np.uint8)     # Image to draw the contours
    # image, contours, hierarchy =   cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # for cnt in contours:
    #     color = np.random.randint(0,255,(3)).tolist()  # Select a random color
    #     cv2.drawContours(drawing,[cnt],0,color,2)
    #     # cv2.imshow('output',drawing)
    # # cv2.imwrite('img.jpg', drawing)
    return img,edges


def main():
	img = cv2.pyrDown(cv2.pyrDown(cv2.imread('bit3.jpg')))

	height, width, channels = img.shape

	middle = width/2
	lm = width*.4
	rm = width-(width*.4)

	leftmid = int(lm)
	rightmid = int(rm)
	inc = rightmid-leftmid
	nextinc = inc
	var = []
	crop_img = img[0:height, leftmid:rightmid]

	height, width, channels = crop_img.shape
	previnc = 0
	

	thresh = 100
	for x in range(0,4):
		newcrop = crop_img[previnc:nextinc, 0:width]
		gray = cv2.cvtColor(newcrop,cv2.COLOR_BGR2GRAY)
		blur = cv2.GaussianBlur(gray,(5,5),0)
		out,edges = thresh_callback(thresh, blur, newcrop)
		cv2.imwrite('croped'+str(x)+'.jpg',newcrop)

		previnc += inc
		nextinc += inc
		plt.subplot(240+x+1)
		plt.imshow(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))
		plt.subplot(240+x+5)
		plt.imshow(edges, cmap = 'gray')
		cv2.imwrite('edges'+str(x)+'.jpg',edges)
		cv2.imwrite('lines'+str(x)+'.jpg',out)
		var = np.append(var,[out])

	plt.show()


  # max_thresh = 255


if __name__ == '__main__':
    main()







