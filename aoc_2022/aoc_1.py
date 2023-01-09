with open('aoc_1_data') as f:
    data = f.readlines()

import numpy as np

num = 0
total = 0
res = {}
dt = [int(str(x).rstrip('\n')) if len(str(x).rstrip('\n')) > 0 else -1 for x in data]
for i in range(len(dt)):
    if dt[i] > 0:
        total += dt[i]
    else:
        res.update({num: total})
        total = 0
        num += 1

np_dt = np.array([x for x in res.values()])

print(np_dt.max())

high1 = np_dt.max()

np_filt = np.concatenate([np_dt[0:np_dt.argmax()], np_dt[np_dt.argmax() + 1:]])
high2 = np_filt.max()

np_filt2 = np.concatenate([np_filt[0:np_filt.argmax()], np_filt[np_filt.argmax() + 1:]])
high3 = np_filt2.max()

print(high1 + high2 + high3)
