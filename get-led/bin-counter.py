import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

leds = [24, 22, 23, 27, 17, 25, 12, 16]
for led in leds:
    GPIO.setup(led, GPIO.OUT)
    GPIO.output(led, 0)

UP_BTN = 5
DOWN_BTN = 6

GPIO.setup(UP_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DOWN_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

num = 0
sleep_time = 0.2

def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def update_leds(value):
    bits = dec2bin(value)
    for i in range(8):
        GPIO.output(leds[i], bits[i])

update_leds(0)

try:
    while True:
        if GPIO.input(UP_BTN) == 0:
            num = (num + 1) % 256
            print(num, dec2bin(num))
            update_leds(num)
            time.sleep(sleep_time)
        
        if GPIO.input(DOWN_BTN) == 0:
            num = (num - 1) % 256
            print(num, dec2bin(num))
            update_leds(num)
            time.sleep(sleep_time)
        
        time.sleep(0.01)

except KeyboardInterrupt:
    GPIO.cleanup()