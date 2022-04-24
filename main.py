from apscheduler.schedulers.background import BlockingScheduler
import logging
import clanbattle
root = logging.getLogger()
root.setLevel(logging.INFO)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    scheduler = BlockingScheduler(timezone="Asia/Shanghai")
    scheduler.add_job(clanbattle.stage_data, 'interval', minutes=30, start_date="2022-04-24 5:01:00", end_date="2022-04-29 23:51:00")
    scheduler.start()
