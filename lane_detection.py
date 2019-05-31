import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while 1:
    # Take each frame
    frame = cap.read()
    # Greyscale
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Define range of colour in purple lanes
    lower_purple = np.array([269, 100, 50])
    upper_purple = np.array([269, 100, 50])

    mask = cv2.inRange(hsv, lower_purple, upper_purple)
    res = cv2.bitwise_and(frame, frame, mask = mask)
    
