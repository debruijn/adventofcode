import numpy as np

with open('aoc_1_data') as f:
    data = f.readlines()

data = [str(x).rstrip('\n') for x in data]
data = np.array(data).astype(int)

print(sum(data[1:] > data[:-1]))

data_sum = data[:-2] + data[1:-1] + data[2:]

print(sum(data_sum[1:] > data_sum[:-1]))
