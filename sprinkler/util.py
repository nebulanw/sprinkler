from sprinkler.motor import Motor
from sprinkler.sensor import Sensor
from sprinkler.weather import Weather
from sprinkler.return_codes import WateringReturnCodes
from sprinkler.db import db_log, db_metrics, db_config
import time

initial_configs = db_config.get_config()

motor = Motor(initial_configs['motor_pin'])
sensor = Sensor(initial_configs['sensor_pin'])
weather = Weather(
    initial_configs['latitude'],
    initial_configs['longitude'],
    initial_configs['timezone']
)

def water(code):
    """Runs the pump for one irrigation cycle if it's not already running."""

    if db_log.get_watering() == True:
        return False
    db_log.update_watering(True)
    motor.start()
    time.sleep(db_config.get_config()['watering_time'])
    motor.stop()
    db_log.update_watering(False)
    db_log.log_watering(code.value)
    metrics = db_metrics.get_metrics()
    metrics['watered_yesterday'] = True
    db_metrics.update_metrics(metrics)
    return True

def manual_water():
    water(WateringReturnCodes.MANUAL)

def check_water(sensor_ok_days: int) -> tuple[bool, WateringReturnCodes]:
    """Checks watering criteria. Returns `True, <sprinkler.return_codes.WaterReturnCodes>` if passed."""
    metrics = db_metrics.get_metrics()
    if metrics['watered_yesterday'] == True:
        metrics['watered_yesterday'] = False
        db_metrics.update_metrics(metrics)
        return False, WateringReturnCodes.EXIT_CONSEC
    forecast = weather.query()
    cfg = db_config.get_config()
    if (forecast.current_precipitation >= cfg['precipitation_threshold']
         or forecast.total_precipitation >= cfg['precipitation_threshold']):
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
    metrics = db_metrics.get_metrics()
    should_water, code = check_water(metrics['days_since_sensor_humid'])

    if should_water:
        water(code)
    else:
        db_log.log_watering(code.value)
    metrics = db_metrics.get_metrics()
    if code in [
        WateringReturnCodes.EXIT_WEATHER,
        WateringReturnCodes.EXIT_CONSEC,
        WateringReturnCodes.OK_SENSOR_BYPASS,
        WateringReturnCodes.OK
    ]:
        metrics['days_since_sensor_humid'] = 0
    else:
        metrics['days_since_sensor_humid'] += 1

    db_metrics.update_metrics(metrics)

def stop_motor():
    motor.stop()

def check_sensor():
    return sensor.query()
