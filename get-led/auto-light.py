import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
led = 26
GPIO.setup(led, GPIO.OUT)
photo_pin = 0

GPIO.setup (photo_pin, GPIO.IN)

while True:
    GPIO.output (led, not GPIO.output(photo_pin))
    time.sleep (0.05)
