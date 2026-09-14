from sprinkler import util
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import datetime

daily_trigger = CronTrigger(hour='8')
test_trigger = CronTrigger(second='0-59/15')

class Tasks:
    def start(self):
        self.scheduler = BackgroundScheduler(
            executors={"default": ThreadPoolExecutor(2)},
            job_defaults={'misfire_grace_time': 15 * 60}
        )
        self.scheduler.start()

        self.scheduler.add_job(util.scheduled_water, daily_trigger, id="util.scheduled_water", max_instances=1)

    def shutdown(self):
        self.scheduler.remove_all_jobs()
        self.scheduler.shutdown()

    def run_now(self, job_id: str):
        self.scheduler.get_job(job_id=job_id).modify(next_run_time=datetime.datetime.now())

    def create_temp_job(self, func):
        self.scheduler.add_job(func, 'date', run_date=datetime.datetime.now())
