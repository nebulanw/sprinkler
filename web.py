from sprinkler.db import db_config, db_log, db_metrics
from sprinkler.tasque import Tasks
from sprinkler.util import stop_motor, manual_water, check_sensor
from sprinkler.request_schemas import UpdateSettingsSchema
from flask import Flask, request, jsonify, abort, render_template
import atexit

tasks = Tasks()
tasks.start()
update_settings_schema = UpdateSettingsSchema()
app = Flask(__name__)

def shutdown():
    print("Running cleanup")
    tasks.shutdown()
    stop_motor()
    import RPi.GPIO as GPIO
    GPIO.cleanup()

atexit.register(shutdown)

@app.route('/')
def root():
    return render_template("dash.html")

@app.route('/api/logs', methods=['GET'])
def get_logs():
    return db_log.get_logs()

@app.route('/api/status', methods=['GET'])
def get_status():
    return {'watering': db_log.get_watering()}

@app.route('/api/water_now', methods=['GET'])
def get_water_now():
    is_free = not db_log.get_watering()
    if is_free:
        tasks.create_temp_job(manual_water)
    return {'success': is_free}

@app.route('/api/settings', methods=['GET'])
def get_settings():
    return db_config.get_config()

@app.route('/api/settings', methods=['POST'])
def post_settings():
    reqj = request.json
    if reqj is None:
        abort(400)
    errors = update_settings_schema.validate(reqj)
    if errors:
        return jsonify(errors), 400
    db_config.update_config(reqj)
    return 'ok'

@app.route('/api/sensor')
def get_sensor():
    return {'state': check_sensor()}

app.run()
