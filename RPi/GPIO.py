# RPi.GPIO stubs

BCM = "GPIO.BCM"
OUT = "GPIO.OUT"
LOW = "GPIO.LOW"
HIGH = "GPIO.HIGH"

def setup(*args):
    pass

def setmode(*args):
    pass

def input(*args):
    from builtins import input as input_orig
    return input_orig("GPIO.input() answer?") == 'True'

def output(pin, val):
    print(f"Pin {pin} set to {val}")
