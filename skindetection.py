# Dora Jambor
# February 2016 Spring 1's Recurse Center

# Built upon the 'pyimagesearch' opencv tutorials 
# http://www.pyimagesearch.com/2014/08/18/skin-detection-step-step-example-using-python-opencv/

'''
Skindetection with OpenCV. The color range is messy, so will only work with minimal noise in the background.
Three webcam displays: normal, masked, hsv color space
'''


import numpy as np
import cv2
import automation

# # color region in BGR
# upper  = cv2.cvtColor(np.uint8([[[10,63, 255]]]),cv2.COLOR_BGR2HSV)
# lower  = cv2.cvtColor(np.uint8([[[144,169, 237]]]),cv2.COLOR_BGR2HSV)

# color region in HSV BLUE
# lower = np.array([0, 70, 120], dtype = "uint8")
# upper = np.array([30, 255, 220], dtype = "uint8")
lower = np.array([100,100,100])
upper = np.array([120,255,255])


def move():
	if len(centerArray) > 1:
		# first coordinate is width, 2nd is height
		# if j coordinate is larger, center moved down, right is left for the cam
		if centerArray[-1][0] <= centerArray[-2][0] & centerArray[-1][1] <= centerArray[-2][1]:
			print "Moving up right..."
		elif centerArray[-1][0] <= centerArray[-2][0] & centerArray[-1][1] >= centerArray[-2][1]:
			print "Moving down right..."
		elif centerArray[-1][0] >= centerArray[-2][0] & centerArray[-1][1] <= centerArray[-2][1]:
			print "Moving up left..."
		elif centerArray[-1][0] >= centerArray[-2][0] & centerArray[-1][1] >= centerArray[-2][1]:
			print "Moving down left..."
		print centerArray[-1][0], centerArray[-2][0]
		print centerArray[-1][1], centerArray[-2][1]
		# only save the last center
		return [centerArray[-1]]


def read(centerArray):
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

	# myobject = []
	# if round >= 1:
	# ---------------------------------------------------------- new stuff
		# start_width = skin.shape[1] / 4
		# end_width = skin.shape[1] / 4*3
		# start_height = skin.shape[0] / 6
		# end_height = skin.shape[0] / 6*5

		# for i in range(0, skin.shape[1],5):
		# 	for j in range(0, skin.shape[0],5):
		# 		if i not in range(start_width, end_width):
		# 			# check if in range of skin color region
		# 			if 0 < skin[j,i][0]  < 55:
		# 				if 70 < skin[j,i][1]  < 255:
		# 					if 70 < skin[j,i][2]  < 225:
		# 						myobject.append(skin[j,i])
		# 		if j not in range(start_height, end_height):
		# 			if 0 < skin[j,i][0]  < 55:
		# 				if 70 < skin[j,i][1]  < 255:
		# 					if 70 < skin[j,i][2]  < 225:
		# 						myobject.append(skin[j,i])

	# ----------------------------------------------------------
	# finding contour, drawing circle around it, find radius & center
	cnts = cv2.findContours(mask, cv2.RETR_TREE,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None

	# only proceed if at least one contour was found --> cnts is a list of arrays containing points: 
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		# return c, the largest array in cnts containing [[[x,y]]] points
		c = max(cnts, key=cv2.contourArea)
		cnt = contour[c]
		hull = cv2.convexHull(cnt)
		drawing = np.zeros(resized.shape,np.uint8)
		cv2.drawContours(drawing,[cnt],0,(0,255,0),2)
		cv2.drawContours(drawing,[hull],0,(0,0,255),2)

		# # c.shape looks like: [[[1,2], [1,3], [2,3]]] -> triple brackets taken from cnts notation. 
		# # only proceed if more than 2 point found.
		# if  len(c.shape) > 2:
		# 	# & c.shape[1] == 1 & c.shape[2] == 2
		# 	# ------------------ Code used for non-circle objects (aka enclosing shape) ------------------
		# 	# M = cv2.moments(c)
		# 	# center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# 	((x, y), radius) = cv2.minEnclosingCircle(c)
		# 	center = (int(x),int(y))
		# 	if radius > 10:
		# 		# draw the circle and centroid on the frame,
		# 		# then update the list of tracked points
		# 		cv2.circle(resized, (int(x), int(y)), int(radius),
		# 			(0, 255, 255), 2)
		# 		cv2.circle(resized, center, 5, (0, 0, 255), -1)

			
		# 	automation.mousemove(center)

			# every 25 frame add center to array for movement check
			if round%50 == 0:
				centerArray.append(center)
				centerArray = move()

			# only proceed if the radius meets a minimum size
			

		# ----------------------------------------------------------

		# imshow always goes with waitKey: waitKey displays 
		# the given frame for 'arg' miliseconds. If it's zero, it displays one frame for an infinite amount of time
		# if it's 1 it displays each frame for one milisecond- in which it waits for a key event. If key event not given, 
		# it returns -1 and the window keeps running.
		cv2.imshow('skin', np.hstack([resized, skin, hsv]))





if __name__ == "__main__":
	# Construct Camera
	camera = cv2.VideoCapture(0)
	round = 0
	centerArray = []
	while True:
		if read(centerArray) != False:
			round += 1
			# ord is to convert string to int
		else:
			break
		key = cv2.waitKey(25) & 0xFF 
		if key == ord('q'):
			break
	cv2.destroyAllWindows()

