import numpy as np
import cv2
from PIL import Image
import time
"""
NOTE: THIS FILE IS DEPRECATED AND KEPT ONLY FOR REFERENCE REASONS. PLEASE USE lane_det_working.py
"""

def gaussian_blur(img, kernel_size):
	"""Applies a Gaussian Noise Reduction effect"""
	return cv2.GaussianBlur(img, (kernel_size, kernel_size), kernel_size)


cap = cv2.VideoCapture(0)
iterator = 0
while True:
	# capture frame-by-frame
	ret, frame = cap.read()

	# Greyscale
	grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	# lower_purple = np.asarray([300, 100, 50], dtype='uint8')
	# upper_purple = np.asarray([310, 100, 50], dtype='uint8')
	# mask_purple = cv2.inRange(frameHSV, lower_purple, upper_purple)
	RGBGrey = cv2.cvtColor(grey, cv2.COLOR_GRAY2RGB)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	lower_blue = np.array([110, 50, 50])
	upper_blue = np.array([130, 255, 255])
	mask = cv2.inRange(hsv, lower_blue, upper_blue)
	lower_black = np.asarray([0, 0, 0])
	upper_black = np.asarray([180, 255, 30])
	black_mask = cv2.inRange(hsv, lower_black, upper_black)
	res = cv2.bitwise_and(frame, frame, mask=mask)
	blackres = cv2.bitwise_and(frame, frame, mask=black_mask)
	kernel_size = 5
	low_threshold = 50
	high_threshold = 150
	canny_edges = cv2.Canny(blackres, 50, 150)
	gaussBlur = gaussian_blur(canny_edges, 5)
	iterator += iterator
	if iterator >= 10:
		break


cap.release()
cv2.destroyAllWindows()
