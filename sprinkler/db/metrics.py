from tinydb import TinyDB, Query

# Program metrics
DAYS_SINCE_SENSOR_HUMID = 0

class Database:
    def __init__(self, db_file: str):
        self.db = TinyDB(db_file)
        self.initialize_db()

    def initialize_db(self):
        if self.db.all() == []:
            self.db.insert({
                'metrics': {
                    'days_since_sensor_humid': DAYS_SINCE_SENSOR_HUMID,
                    'watered_yesterday': False
                }
            })

    def update_metrics(self, new_metrics):
        self.db.update({'metrics': new_metrics})

    def get_metrics(self):
        return self.db.get(Query().metrics.exists())['metrics']