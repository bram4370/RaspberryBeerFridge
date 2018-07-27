import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers

RELAIS_1_GPIO = 26
LED_1_GPIO = 21

GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
GPIO.setup(LED_1_GPIO, GPIO.OUT)

GPIO.output(LED_1_GPIO, GPIO.HIGH)
GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # out
time.sleep(2)
GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # on

GPIO.cleanup()
