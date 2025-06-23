import RPi.GPIO as GPIO

class Motor:
    def __init__(self, relay_pin: int = 27):
        self.RELAY_PIN = 27

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.RELAY_PIN, GPIO.OUT)
        GPIO.output(self.RELAY_PIN, GPIO.LOW)

    def start(self):
        GPIO.output(self.RELAY_PIN, GPIO.HIGH)

    def stop(self):
        GPIO.output(self.RELAY_PIN, GPIO.LOW)

    def destroy(self):
        GPIO.output(self.RELAY_PIN, GPIO.LOW)
