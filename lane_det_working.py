# importing useful packages.
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
import numpy as np
import cv2
import math
import os
from PIL import Image  # As cv2.imshow() fails on all OSs, we use this instead.
import time


def grayscale(img):  # Applies greyscale transform. Returns image with only one colour channel.
	"""
	NOTE: To see image as greyscaled, call with show_image
	:param img: Image to be applied
	:return: Greyscaled image
	"""
	return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def canny(img, low_threshold, high_threshold):
	"""Applies the Canny transform"""
	return cv2.Canny(img, low_threshold, high_threshold)


def gaussian_blur(img, kernel_size):
	"""Applies a Gaussian Noise kernel"""
	return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)


def region_of_interest(img, vertices):  # Taken from external source
	"""
	Applies an image mask.
	Only keeps the region of the image defined by the polygon
	formed from `vertices`. The rest of the image is set to black.
	"""
	# defining a blank mask to start with
	mask = np.zeros_like(img)
	
	# defining a 3 channel or 1 channel color to fill the mask with depending on the input image
	if len(img.shape) > 2:
		channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
		ignore_mask_color = (255,) * channel_count
	else:
		ignore_mask_color = 255
	
	# filling pixels inside the polygon defined by "vertices" with the fill color
	cv2.fillPoly(mask, vertices, ignore_mask_color)
	
	# returning the image only where mask pixels are nonzero
	masked_image = cv2.bitwise_and(img, mask)
	return masked_image


def draw_lines(img, lines, color=[255, 255, 255], thickness=7):  # Took this function from online
	"""
	NOTE: this is the function you might want to use as a starting point once you want to
	average/extrapolate the line segments you detect to map out the full
	extent of the lane (going from the result shown in raw-lines-example.mp4
	to that shown in P1_example.mp4).
	Think about things like separating line segments by their
	slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
	line vs. the right line.  Then, you can average the position of each of
	the lines and extrapolate to the top and bottom of the lane.
	This function draws `lines` with `color` and `thickness`.
	Lines are drawn on the image inplace (mutates the image).
	If you want to make the lines semi-transparent, think about combining
	this function with the weighted_img() function below
	"""
	for line in lines or []:  # FIXME: Python error: NoneType is not iterable
		for x1, y1, x2, y2 in line:
			cv2.line(img, (x1, y1), (x2, y2), color, thickness)


def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):  # img should be an image with canny transform.
	lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len,
	                        maxLineGap=max_line_gap)
	line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
	draw_lines(line_img, lines)
	return line_img  # Returns an image with lines drawn


def weighted_img(img, initial_img, α=0.8, β=1., λ=0.):  # Taken from external source
	"""
	`img` is the output of the hough_lines(), An image with lines drawn on it.
	Should be a blank image (all black) with lines drawn on it.
	`initial_img` should be the image before any processing.
	The result image is computed as follows:
	initial_img * α + img * β + λ
	NOTE: initial_img and img must be the same shape!
	"""
	return cv2.addWeighted(initial_img, α, img, β, λ)


def process_frame(image):
	global first_frame
	
	gray_image = grayscale(image)
	img_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
	# hsv = [hue, saturation, value]
	# more accurate range for colour identification than RGB
	
	lower_black = np.asarray([0, 0, 0])  # Lower bound for identifying black
	upper_black = np.asarray([180, 255, 30])  # Upper bound
	black_mask = cv2.inRange(img_hsv, lower_black, upper_black)  # Mask on original image to be combined with
	# greyscale image
	mask_bg_image = cv2.bitwise_and(gray_image, black_mask)  # Combined greyscale and black-identified image
	
	kernel_size = 5  # Kernel blur scaling. 5 is best value
	gauss_gray = gaussian_blur(mask_bg_image, kernel_size)  # Gaussian blur averages pixel values to make it easier on
	# canny()
	
	# Threshold values for canny edge detection
	low_threshold = 50
	high_threshold = 150
	canny_edges = canny(gauss_gray, low_threshold, high_threshold)
	
	"""
	This part is for identifying the part of the image we don't need (that being the upper half) and removing it.
	Draws a Region of Interest polygon and covers the top half of the image to not screw up canny and other functions.
	"""
	imshape = image.shape
	lower_left = [imshape[1] / 9, imshape[0]]
	lower_right = [imshape[1] - imshape[1] / 9, imshape[0]]
	top_left = [imshape[1] / 2 - imshape[1] / 8, imshape[0] / 2 + imshape[0] / 10]
	top_right = [imshape[1] / 2 + imshape[1] / 8, imshape[0] / 2 + imshape[0] / 10]
	vertices = [np.array([lower_left, top_left, top_right, lower_right], dtype=np.int32)]
	roi_image = region_of_interest(canny_edges, vertices)
	
	rho = 2  # Distance resolution of grid in Hough space
	theta = np.pi / 180  # Angular resolution of grid in Hough space
	threshold = 20  # minimum number of intersections in a grid for candidate line to go to output
	min_line_len = 50
	max_line_gap = 200
	
	line_image = hough_lines(roi_image, rho, theta, threshold, min_line_len, max_line_gap)
	result = weighted_img(line_image, image, α=0.8, β=1., λ=0.)
	return result


def show_image(img):  # Shows the image. DO NOT CALL IN A LOOP EVER PLEASE FOR THE LOVE OF GOD
	pil_image = Image.fromarray(img)
	pil_image.show()


cap = cv2.VideoCapture(0)  # Captures video stream from your camera
iterator = 0
while True:  # Will run once every 5 seconds, with still frame from video stream
	ret, frame = cap.read()
	show_image(process_frame(frame))
	time.sleep(5)
