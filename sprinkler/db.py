from tinydb import TinyDB, Query
from datetime import datetime

# Configuration options
MOTOR_PIN = 27
SENSOR_PIN = 17
LATITUDE = 0.0000
LONGITUDE = 0.0000
TIMEZONE = "America/Los_Angeles"
PRECIPITATION_THRESHOLD = 0.5
SENSOR_DAY_LIMIT = 4
WATERING_TIME = 300

# Program metrics
DAYS_SINCE_SENSOR_HUMID = 0

class Database:
    def __init__(self, db_file: str):
        self.db = TinyDB(db_file)
        self.initialize_db()

    def initialize_db(self):
        if self.db.all() == []:
            self.db.insert({
                'config': {
                    'motor_pin': MOTOR_PIN,
                    'sensor_pin': SENSOR_PIN,
                    'latitude': LATITUDE,
                    'longitude': LONGITUDE,
                    'timezone': TIMEZONE,
                    'precipitation_threshold': PRECIPITATION_THRESHOLD,
                    'sensor_day_limit': SENSOR_DAY_LIMIT,
                    'watering_time': WATERING_TIME
                },
                'metrics': {
                    'days_since_sensor_humid': DAYS_SINCE_SENSOR_HUMID
                },
                'logs': []
            })

    def update_config(self, new_config):
        self.db.update({'config': new_config})

    def update_metrics(self, new_metrics):
        self.db.update({'metrics': new_metrics})

    def log_watering(self, code: int):
        log_entry = {
            'date': datetime.now().isoformat(),
            'code': code
        }
        self.db.update({'logs': [log_entry] + self.db.get(Query().logs.exists())['logs'] })

    def get_config(self):
        return self.db.get(Query().config.exists())['config']

    def get_metrics(self):
        return self.db.get(Query().metrics.exists())['metrics']

    def get_logs(self):
        return self.db.get(Query().logs.exists())['logs']
