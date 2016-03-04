'''
Color conversion
Three webcam displays: normal, masked, masked with original color
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
	width = 300.0 / frame.shape[1]
	dim = (300, int(frame.shape[0] * width))
	return cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

def color(frame):
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, lower, upper)
	return cv2.bitwise_and(frame, frame, mask=mask)


def loop():
	while True:
		resized = get_frame()
		result = color(resized)
		# print_stuff(resized, iter)
		# iter += 1
		cv2.imshow('frame', np.hstack([resized, result]))

		key = cv2.waitKey(25) & 0xFF
		if key == ord('q'):
			break


if __name__ == "__main__":
	# Construct Camera
	camera = cv2.VideoCapture(0)
	loop()