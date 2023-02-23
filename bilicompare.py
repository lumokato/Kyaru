import pandas as pd
import pickle
import time
import csv
import os
import random
import base64
import json
import aiohttp
import asyncio


# 获取bili数据
async def bilipage(page):
    with open('api.json', encoding='utf-8') as fp:
        api_data = json.load(fp)
    a = api_data["code_a"]
    b = api_data["code_b"]
    c, r, t, s = "", "", str(int(time.time())), "".join(
        random.sample("".join([chr(x).lower() for x in range(65, 91)]), 11))
    for i in s + t:
        c += a[i]
    for i in base64.b64encode(c.encode()).decode():
        r += b[i]
    urlroot = api_data["url"]
    default_headers = {
        # "accept": 'application/json, text/plain, */*',
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        # "Custom-Source": "KyoukaOfficial",
        # "Content-Type": "application/json",
        "Origin": "https://kyouka.kengxxiao.com/",
        # "Sec-Ch-Ua": "Chromium",
        # "Sec-Fetch-Site": "cross-site",
        # "Sec-Fetch-Mode": "cors",
        # "Sec-Fetch-Dest": "empty",
        "Referer": "https://kyouka.kengxxiao.com/",
        # "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        # "Accept": "application/json, text/plain, */*",
        # "Accept-Encoding": "gzip, deflate, br",
        # "Connection": "close",
        "x-nonce": s,
        "x-timestamp": t,
        "x-sign": f"SIGv1.0|{r}"
    }
    request = {
        "name": "",
        "leaderName": "",
        "minRank": 1,
        "maxRank": 99999,
        "score": 0,
        "page": page,
        "period": 0,
        "maxPerPage": 100,
        "fav": False,
        "onlyRank": False
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(urlroot + '/clan/rankSearch/', json=request, headers=default_headers) as resp:
                res = await resp.json()
                return res["data"]["clans"]
    except Exception:
        return False


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
            rank_list.append(binarySearch(
                score_list, 0, len(score_list)-1, score))

        qd_data.insert(loc=len(qd_data.columns),
                       column='bili_rank', value=rank_list)
        qd_data.to_csv('qd/history/1/' + month)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(bilipage(4))
    loop.close()
    cal_rank()
