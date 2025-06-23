import RPi.GPIO as GPIO

class Sensor:
    def __init__(self, sensor_pin: int = 17):
        self.SENSOR_PIN = sensor_pin

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SENSOR_PIN, GPIO.IN)

    def query(self) -> bool:
        """Returns `True` if below threshold, `False` otherwise."""
        # 0: threshold (green), 1: below threshold (off)
        #print(GPIO.input(self.SENSOR_PIN))
        x = GPIO.input(self.SENSOR_PIN) == True
        #x = bool(0 == 0)
        print(f"I got {x}")
        return x
