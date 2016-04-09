# Dora Jambor
# February 2016 Spring 1's Recurse Center

# Based on the 'pyimagesearch' opencv tutorials 
# http://www.pyimagesearch.com/2014/09/01/build-kick-ass-mobile-document-scanner-just-5-minutes/

'''
Edge detection with OpenCV - can be used as a scanner. Prep for MNIST digit recognition
Two webcam displays: thresh and edged
'''

import numpy as np
import cv2

# Construct Camera
camera = cv2.VideoCapture(0)

while True:
	(ret, frame) = camera.read()

	# resizing dimensions - shape[1] is for the width
	width = 600.0 / frame.shape[1]
	dim = (600, int(frame.shape[0] * width))
	resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

	# edge detection on gray scale
	gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)	
	gray = cv2.GaussianBlur(gray, (5, 5), 0)

	# convert into binary color space
	ret,thresh = cv2.threshold(gray,127,255,0)	
	edged = cv2.Canny(gray, 75, 200)

	# finding contours: first you need black and white spcae --> source image called thresh
	# Each individual contour is a Numpy array of (x,y) coordinates of boundary points of the object.
	# last argument deletes those points that represent a line, and instead keep the main edge points
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None

	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(resized, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(resized, center, 5, (0, 0, 255), -1)

	cv2.imshow('frames', np.hstack([thresh, edged]))

	# ord is to convert string to int
	key = cv2.waitKey(25) & 0xFF 
	if key == ord('q'):
		break

cv2.destroyAllWindows()
