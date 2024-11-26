import os
import logging

from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from wrappers import FootballDataApiWrapper
from models import Match

logging.basicConfig(
    level=logging.INFO,
    format="%(name)s - %(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


def collect_data():
    logger.info("Data collection started")
    football_api = FootballDataApiWrapper(os.environ.get("API_KEY"))
    matches = football_api.fecth_matches()["matches"]
    results = Match.bulk_upsert(matches)
    logger.info(f"Data collection task done. Results: {results}")


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(collect_data, CronTrigger(hour=1, minute=00, second=00))
    scheduler.start()
