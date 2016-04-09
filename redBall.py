# Dora Jambor
# February 2016, Recurse Center

'''
Tracks a red ball, and draws contours around it. Use automation.py if you want to map it to your mouse.
Two webcam displays: normal and bitwise masked (with original color)
'''
import numpy as np
import cv2

# this should be RED!!!!!!!!!!!!!!! in HSV
lower= np.array([160, 150,110])
upper = np.array([180,255,255])

# upper  = cv2.cvtColor(np.uint8([[[0,0, 255]]]),cv2.COLOR_BGR2HSV)
# lower  = cv2.cvtColor(np.uint8([[[37,27, 132]]]),cv2.COLOR_BGR2HSV)

def get_frame():
	(ret, frame) = camera.read()

	# resizing dimensions - shape[1] is for the width
	width = 600.0 / frame.shape[1]
	dim = (600, int(frame.shape[0] * width))
	return cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

def color(frame):
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, lower, upper)
	return mask

def loop():
	while True:
		resized = get_frame()
		mask = color(resized)
		result = cv2.bitwise_and(resized, resized, mask=mask)

		# -------------------------- contours --------------------------
		cnts = cv2.findContours(mask, cv2.RETR_TREE,
				cv2.CHAIN_APPROX_SIMPLE)[-2]
		center = None

		# only proceed if at least one contour was found --> cnts is a list of arrays containing points: 
		if len(cnts) > 0:		
		# 	# return c, the largest array in cnts containing [[[x,y]]] points
			c = max(cnts, key=cv2.contourArea)

		# 	c.shape looks like: [[[1,2], [1,3], [2,3]]] -> triple brackets taken from cnts notation. 
		# 	only proceed if more than 2 points found.
			if  len(c.shape) > 2:
				((x, y), radius) = cv2.minEnclosingCircle(c)
				center = (int(x),int(y))
				if radius > 10:
					# draw the circle and centroid on the frame,
					# then update the list of tracked points
					cv2.circle(resized, (int(x), int(y)), int(radius),
						(0, 255, 255), 2)
					cv2.circle(resized, center, 5, (0, 0, 255), -1)
		cv2.imshow('frame', np.hstack([resized, result]))
		key = cv2.waitKey(25) & 0xFF
		if key == ord('q'):
			break


if __name__ == "__main__":
	# Construct Camera
	camera = cv2.VideoCapture(0)
	loop()