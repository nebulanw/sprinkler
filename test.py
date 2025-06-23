import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN)

try:
    while True:
        print(GPIO.input(16))
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()

