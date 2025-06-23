import RPi.GPIO as GPIO
import time

class Sensor:
    def __init__(self, sensor_pin: int = 17):
        self.SENSOR_PIN = sensor_pin
        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SENSOR_PIN, GPIO.IN)

    def true_query(self) -> bool:
        """Returns `True` if below threshold, `False` otherwise."""
        # 0: threshold (green), 1: below threshold (off)
        x = GPIO.input(self.SENSOR_PIN) == 0
        return x

    def query(self) -> bool:
        t = 0
        f = 0
        for _ in range(9):
            time.sleep(0.1)
            if self.true_query() is True:
                t += 1
            else:
                f += 1

        return f > t
