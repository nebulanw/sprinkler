from enum import Enum

class WateringReturnCodes(Enum):
    OK = 0
    OK_SENSOR_BYPASS = 1
    EXIT_WEATHER = 2
    EXIT_SENSOR = 3
    MANUAL = 4
    EXIT_CONSEC = 5
