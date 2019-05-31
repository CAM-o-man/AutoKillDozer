import RPi.GPIO as GPIO
import time
import pyrebase
servoPIN = 33

# Firebase config
config = {
	"apiKey": "AIzaSyASTUIz2eB94GndHYs_QiGYB3304AF7yxk",
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
value = db.child("rt").get().val()
left = db.child("lft").get().val()
reset = db.child("reset").get().val()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoPIN, GPIO.OUT)
GPIO.setwarnings(False)

p = GPIO.PWM(servoPIN, 50)  # GPIO 17 for PWM with 50Hz
p.start(7.5)  # Initialization
dutycycle = 0
try:
	while True:
		value = db.child("rt").get().val()
		left = db.child("lft").get().val()
		print(left)
		if value:
			print("Inside if")
			p.ChangeDutyCycle(2.5)
			time.sleep(0.2)
			dutycycle = 2.5

			print("Changed duty cycle")
		if left:
			print("Inside if")
			p.ChangeDutyCycle(12.5)
			time.sleep(0.2)
			dutycycle = 7.5

		if reset == True:
			p.ChangeDutyCycle(2.5)
			time.sleep(0.2)




except KeyboardInterrupt:
	p.stop()
	GPIO.cleanup()
