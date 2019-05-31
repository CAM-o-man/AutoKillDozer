import RPi.GPIO as GPIO
import time
import pyrebase
# Firebase config
config = {
    "apikey":"AIzaSyASTUIz2eB94GndHYs_QiGYB3304AF7yxk",
    "authDomain": "makers2018-e66f3.firebaseapp.com",
    "databaseURL": "https://makers2018-e66f3.firebaseio.com",
    "projectId": "makers2018-e66f3",
    "storageBucket": "makers2018-e66f3.appspot.com",
    "messagingSenderId": "1063415680253",
    "appId": "1:1063415680253:web:3163d6d1dc0481c7"
}
firebase = pyrebase.initialize_app(config)
# Database init
db = firebase.database()
servoPIN = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoPIN, GPIO.OUT)
GPIO.setwarnings(False)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(7.5) # Initialization
try:
    while True:
        p.ChangeDutyCycle(5)
        time.sleep(0.5)
        p.ChangeDutyCycle(7.5)
        time.sleep(0.5)
        p.ChangeDutyCycle(10)
        time.sleep(0.5)
        p.ChangeDutyCycle(12.5)
        time.sleep(0.5)
        p.ChangeDutyCycle(10)
        time.sleep(0.5)
        p.ChangeDutyCycle(7.5)
        time.sleep(0.5)
        p.ChangeDutyCycle(5)
        time.sleep(0.5)
        p.ChangeDutyCycle(2.5)
        time.sleep(0.5)
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
