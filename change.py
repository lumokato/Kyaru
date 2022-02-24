import os
import clanbattle
import pandas as pd


def change_damage():
    lst = os.listdir('qd/1/')
    for file in lst:
        data = pd.read_csv('qd/1/' + file, index_col=0)
        for i in range(data.shape[0]):
            status = clanbattle.boss_status(data.loc[i, 'damage'])
            data.loc[i:, ('lap', 'boss_id', 'remain')] = [status[0], status[1], status[2]]
        df = pd.DataFrame(data)
        df.to_csv('qd/1/'+file)


if __name__ == '__main__':
    change_damage()
