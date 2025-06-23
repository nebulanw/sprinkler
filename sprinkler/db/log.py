from tinydb import TinyDB, Query
from datetime import datetime

class Database:
    def __init__(self, db_file: str):
        self.db = TinyDB(db_file)
        self.initialize_db()

    def initialize_db(self):
        if self.db.all() == []:
            self.db.insert({
                'logs': [],
                'watering': False
            })

    def update_watering(self, new_watering):
        self.db.update({'watering': new_watering})

    def log_watering(self, code: int):
        log_entry = {
            'date': datetime.now().isoformat(),
            'code': code
        }
        self.db.update({'logs': [log_entry] + self.db.get(Query().logs.exists())['logs'] })

    def get_logs(self):
        return self.db.get(Query().logs.exists())['logs']

    def get_watering(self):
        return self.db.get(Query().watering.exists())['watering']
