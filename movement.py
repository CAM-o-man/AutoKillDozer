import RPi.GPIO as GPIO
import time
import firebase
from firebase import firebase as fire

firebase = firebase.FirebaseApplication('https://makers2018-e66f3.firebaseio.com', None)  # Firebase implemented
result = firebase.get('path/', None)  # Get a value from a node

servoPIN = 18

GPIO.setmode(GPIO.BOARD)

GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(12,50)



