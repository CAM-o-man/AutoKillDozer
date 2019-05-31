import cv2
import numpy as np

cap = cv2.VideoCapture(0)
print("Begin")

while 1:
    # Take each frame
    frame = cap.read()
    print("Capture taken")
    # Greyscale
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Define range of colour in purple lanes
    lower_purple = np.array([269, 100, 50])
    upper_purple = np.array([269, 100, 50])
    print("Converted")

    mask = cv2.inRange(hsv, lower_purple, upper_purple)
    res = cv2.bitwise_and(frame, frame, mask = mask)
    print("Finished")
    # Display Frame
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)

