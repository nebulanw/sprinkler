from sprinkler.motor import Motor
from sprinkler.sensor import Sensor
from sprinkler.weather import Weather
from sprinkler.return_codes import WateringReturnCodes
from sprinkler.db import Database
import time

# TODO: replace constants with config
MOTOR_PIN = 27
SENSOR_PIN = 17
LATITUDE = 47.6418
LONGITUDE = -122.0804
TIMEZONE = "America/Los_Angeles"
PRECIPITATION_THRESHOLD = 0.5
SENSOR_DAY_LIMIT = 5
WATERING_TIME = 300

db = Database("sprinkler.json")

initial_configs = db.get_config()

motor = Motor(initial_configs['motor_pin'])
sensor = Sensor(initial_configs['sensor_pin'])
weather = Weather(
    initial_configs['latitude'],
    initial_configs['longitude'],
    initial_configs['timezone']
)

def check_water(sensor_ok_days: int) -> tuple[bool, WateringReturnCodes]:
    """Checks watering criteria. Returns `True, <sprinkler.return_codes.WaterReturnCodes>` if passed."""
    forecast = weather.query()
    cfg = db.get_config()
    print(forecast.total_precipitation)
    if (forecast.current_precipitation >= cfg['precipitation_threshold']):
         #or forecast.total_precipitation >= cfg['precipitation_threshold']):
        # if percipitation >= 0.5 mm, do not water
        return False, WateringReturnCodes.EXIT_WEATHER
    if sensor.query() == False:
        if sensor_ok_days >= cfg['sensor_day_limit']:
            # if for 5 days straight the sensor is above threshold, water regardless
            return True, WateringReturnCodes.OK_SENSOR_BYPASS
        else:
            return False, WateringReturnCodes.EXIT_SENSOR
    return True, WateringReturnCodes.OK

def scheduled_water():
    """Scheduled watering task."""
    metrics = db.get_metrics()
    cfg = db.get_config()
    should_water, code = check_water(metrics['days_since_sensor_humid'])
    db.log_watering(code.value)
    print(f"{should_water} {code}")
    if should_water:
        motor.start()
        # this feels like bad practice...
        time.sleep(cfg['watering_time'])
        motor.stop()
    if code in [
        WateringReturnCodes.EXIT_WEATHER,
        WateringReturnCodes.OK_SENSOR_BYPASS,
        WateringReturnCodes.OK
    ]:
        metrics['days_since_sensor_humid'] = 0
    else:
        metrics['days_since_sensor_humid'] += 1
    print(f"Days set to {metrics['days_since_sensor_humid']}")
    db.update_metrics(metrics)
    print(db.get_logs())

while True:
    input("Press Enter for next day")
    scheduled_water()
