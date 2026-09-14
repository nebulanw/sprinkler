from tinydb import TinyDB, Query

# Configuration options
MOTOR_PIN = 27
SENSOR_PIN = 16
LATITUDE = 47.571
LONGITUDE = -122.0084
TIMEZONE = "America/Los_Angeles"
PRECIPITATION_THRESHOLD = 0.5
SENSOR_DAY_LIMIT = 4
WATERING_TIME = 30

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
                }
            })

    def update_config(self, new_config):
        self.db.update({'config': new_config})

    def get_config(self):
        return self.db.get(Query().config.exists())['config']
