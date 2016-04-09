# Dora Jambor
# February 2016 Spring 1's Recurse Center

# Based on 'pyimagesearch' opencv tutorials 
# http://www.pyimagesearch.com/2014/08/18/skin-detection-step-step-example-using-python-opencv/

'''
Skindetection with OpenCV. The color range is messy, so will only work with minimal noise in the background.
Three webcam displays: normal, masked, hsv color space
'''

import numpy as np
import cv2
# import automation  only do this for the mouse tracking

# skin color region in HSV  -> still messy - something to refine
lower = np.array([0, 70, 120], dtype = "uint8")
upper = np.array([30, 255, 220], dtype = "uint8")

def read():
	# grab each frame, ret is false if not possible
	(ret, frame) = camera.read()
	if not ret:
		return False

	# resizing dimensions - shape[1] is for the width
	width = 600.0 / frame.shape[1]
	dim = (600, int(frame.shape[0] * width))
	resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

	# frame color space conversion, and region detection
	hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)

	# if in range set pixel to 1, else 0 - binary color conversion
	# apply mask to frame - blur is not necessary, only used for precision
	blur = cv2.GaussianBlur(hsv,(3,3),0)
	mask = cv2.inRange(blur, lower, upper)

	# removing noise by elipse structuring element
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
	mask = cv2.erode(mask, kernel, iterations = 2)
	mask = cv2.dilate(mask, kernel, iterations = 2)

	# bitwise will carry out the add operation with black pixel (FF = 255: 1111111) on original resized frame
	# yielding the original pixels where binary was 1. 
	skin = cv2.bitwise_and(resized, resized, mask=mask)

	# imshow always goes with waitKey: waitKey displays 
	# the given frame for 'arg' miliseconds. If it's zero, it displays one frame for an infinite amount of time
	# if it's 1 it displays each frame for one milisecond- in which it waits for a key event. If key event not given, 
	# it returns -1 and the window keeps running.
	cv2.imshow('skin', np.hstack([resized, skin, hsv]))

if __name__ == "__main__":
	# Construct Camera
	camera = cv2.VideoCapture(0)
	while True:
		read()
		key = cv2.waitKey(25) & 0xFF 
		if key == ord('q'):
			break
	cv2.destroyAllWindows()

