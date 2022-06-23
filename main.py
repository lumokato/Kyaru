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
    shutil.copyfile(os.path.join(dir+'/qd/1', os.listdir(dir+'/qd/1')[-1]), dir+'/qd/history/1/'+str(year)+'年'+str(int(month)-1)+'月.csv')
    shutil.move(dir+'/qd/1', dir+'/qd/history/'+year[-2:]+'-'+'{:0>2d}'.format(int(month)-1))
    os.makedirs(dir+'/qd/1')
    print('o')


def monthly(scheduler):
    clan_time = bilievent.time_battle_bilibili()
    if clan_time:
        scheduler.add_job(move_data, 'date', run_date=clan_time[0]-datetime.timedelta(hours=5))
        scheduler.add_job(clanbattle.stage_data, 'interval', minutes=30, start_date=clan_time[0]+datetime.timedelta(minutes=1), end_date=clan_time[1])


if __name__ == '__main__':
    move_data()
    scheduler = BlockingScheduler(timezone="Asia/Shanghai")
    scheduler.add_job(monthly, 'cron', day='23', hour='17', args=[scheduler])
    scheduler.start()
