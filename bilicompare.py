import pandas as pd
import pickle
import time
import csv
import os


# 将csv格式转换为pkl格式加速加载
def transfer_format():
    start = time.time()
    data = pd.read_csv("a.csv")
    end = time.time()
    print(end-start, "s")
    with open('a.pkl', 'wb') as f:
        pickle.dump(data, f)


# 将总数据拆分为分期结束数据
def split_data():
    data = pd.read_pickle('a.pkl')
    for i in range(12):
        a = data.loc[data['period'] == 1023 + i, "time"]
        print(len(a))
        print(max(a))
        print(len(data.loc[data['time'] == max(a)]))
        b = data.loc[data['time'] == max(a)]
        b.to_csv('qd/history/b/2022年'+str(i+1)+'月.csv')


def binarySearch(arr, left, right, x):
    if right >= left:
        mid = int(left + (right - left)/2)
        if arr[mid] == x:
            return mid
        elif arr[mid] > x:
            return binarySearch(arr, mid+1, right, x)
        else:
            return binarySearch(arr, left, mid-1, x)
    else:
        return left + 1


# 计算对应排名
def cal_rank():
    month_list = os.listdir('qd/history/1')
    for month in month_list:
        qd_data = pd.read_csv('qd/history/1/' + month)
        bili_data = pd.read_csv('qd/history/b/' + month)
        score_list = bili_data['score'].to_list()
        qd_score_list = qd_data['damage'].to_list()
        rank_list = []
        for score in qd_score_list:
            rank_list.append(binarySearch(score_list, 0, len(score_list)-1, score))

        qd_data.insert(loc=len(qd_data.columns), column='bili_rank', value=rank_list)
        qd_data.to_csv('qd/history/2/' + month)


if __name__ == '__main__':
    cal_rank()
