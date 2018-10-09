import socket
import time
import cv2
import numpy as np
import os
import logging
logging.basicConfig(level=logging.DEBUG)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_IP = "10.51.15.2"
UDP_PORT = 5803

cam = cv2.VideoCapture(0)
cam.set(3, 160)
cam.set(4, 120)


def getArea(upperbound, lowerbound):
	ret, frame = cam.read()
	height, width, channels = frame.shape
	hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

	thresh = cv2.inRange(hsv, lower, upper)
	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	maxarea = 0
	centerx = 0
	centery = 0
	contour = 0
	
	for c in contours:
		m = cv2.moments(c)
		if m['m00'] > maxarea:
			centerx = m['m10'] / m['m00']
			centery = m['m01'] / m['m00']
			maxarea = m['m00']
			contour = c

	return cv2.moments(contour)['m00']
	
redUpper = np.array([75, 120, 255])
redLower = np.array([0, 0, 110])

blueUpper = np.array([255, 120, 75])
blueLower = np.array([110, 0, 0])

while True:
    if getArea(redUpper, redLower) > getArea(blueUpper, blueLower):
        sock.sendto(("red"), (UDP_IP, UDP_PORT))
    elif getArea(redUpper, redLower) < getArea(blueUpper, blueLower):
        sock.sendto(("blue"), (UDP_IP, UDP_PORT))

