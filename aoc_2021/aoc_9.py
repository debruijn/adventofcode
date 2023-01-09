import numpy as np

with open('aoc_9_data') as f:
    data = f.readlines()

data = np.array([[int(x) for x in row if x != '\n'] for row in data])

dims = data.shape
low_below = np.concatenate([data[1:, :] - data[:-1, :] > 0, np.ones([1, dims[1]])])
low_above = np.concatenate([np.ones([1, dims[1]]), data[1:, :] - data[:-1, :] < 0])
low_right = np.concatenate([data[:, 1:] - data[:, :-1] > 0, np.ones([dims[0], 1])], axis=1)
low_left = np.concatenate([np.ones([dims[0], 1]), data[:, 1:] - data[:, :-1] < 0, ], axis=1)

local_low = low_below * low_above * low_right * low_left
print(np.sum(data[local_low == 1] + 1))

locs = np.where(local_low == 1)
basin = local_low.copy()
for i in range(len(locs[0])):
    basin[locs[0][i], locs[1][i]] = i + 1

high_below = np.concatenate([data[1:, :] - data[:-1, :] < 0, np.zeros([1, dims[1]])])
high_above = np.concatenate([np.zeros([1, dims[1]]), data[1:, :] - data[:-1, :] > 0])
high_right = np.concatenate([data[:, 1:] - data[:, :-1] < 0, np.zeros([dims[0], 1])], axis=1)
high_left = np.concatenate([np.zeros([dims[0], 1]), data[:, 1:] - data[:, :-1] > 0, ], axis=1)

for i in range(9):
    iter_flow = (data == i) * (basin == 0)
    basin[iter_flow * high_right == 1] = basin[np.concatenate([np.zeros([dims[0], 1]), iter_flow[:, :-1] *
                                                               high_right[:, :-1]], axis=1) == 1]
    basin[iter_flow * high_left == 1] = basin[np.concatenate([iter_flow[:, 1:] * high_left[:, 1:],
                                                              np.zeros([dims[0], 1])], axis=1) == 1]
    basin[iter_flow * high_above == 1] = basin[np.concatenate([iter_flow[1:, :] * high_above[1:, :],
                                                               np.zeros([1, dims[1]])]) == 1]
    basin[iter_flow * high_below == 1] = basin[np.concatenate([np.zeros([1, dims[1]]), iter_flow[:-1, :] *
                                                               high_below[:-1, :]]) == 1]

sums = []
for i in [x for x in np.unique(basin) if x > 0]:
    sums.append(np.sum(basin == i))
    print(f"There are {np.sum(basin == i)} elements in basin {int(i)}")

top3 = sorted(sums, reverse=True)[:3]

print(top3[0] * top3[1] * top3[2])
