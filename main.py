from apscheduler.schedulers.background import BlockingScheduler
import logging
import clanbattle
import bilievent
import datetime
import os
import shutil
root = logging.getLogger()
root.setLevel(logging.INFO)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def move_data():
    year = datetime.datetime.now().strftime("%Y")
    month = datetime.datetime.now().strftime("%m")
    dir = os.getcwd()
    if not os.path.exists(dir+'/qd/history/1/'):
        os.makedirs(dir+'/qd/history/1')
    if os.listdir(dir+'/qd/1'):
        dirname = os.listdir(dir+'/qd/1')
        dirname.sort(key=lambda x: int(x[:-4]))
        shutil.copyfile(os.path.join(dir+'/qd/1', dirname[-1]), dir+'/qd/history/1/'+str(year)+'年'+str(int(month)-1)+'月.csv')
        shutil.move(dir+'/qd/1', dir+'/qd/history/'+year[-2:]+'-'+str(int(month)-1))
        os.makedirs(dir+'/qd/1')


if __name__ == '__main__':
    scheduler = BlockingScheduler(timezone="Asia/Shanghai")
    clan_time = bilievent.time_battle_bilibili()
    scheduler.add_job(move_data, 'date', run_date=clan_time[0]-datetime.timedelta(hours=11))
    scheduler.add_job(clanbattle.stage_data, 'interval', minutes=30, start_date=clan_time[0]+datetime.timedelta(minutes=2), end_date=clan_time[1]+datetime.timedelta(minutes=3))
    scheduler.add_job(clanbattle.stage_data, 'date', run_date=clan_time[1]+datetime.timedelta(days=7), args=[1])
    scheduler.start()
