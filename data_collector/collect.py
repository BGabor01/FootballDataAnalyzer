import os

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from wrappers import FootballDataApiWrapper
from models import Match


def collect_data():
    football_api = FootballDataApiWrapper(os.environ.get("API_KEY"))
    matches = football_api.fecth_matches()["matches"]
    results = Match.bulk_upsert(matches)
    print(results)


if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(collect_data, CronTrigger(hour=1, minute=00, second=00))
    scheduler.start()
