with open('aoc_2_data') as f:
    data = f.readlines()

import numpy as np

data_adj = [str(x).rstrip('\n').replace('A', '1').replace('B', '2').replace('C', '3').replace('X', '1').
            replace('Y', '2').replace('Z', '3').split(' ') for x in data]

np_data = np.matrix(data_adj).astype(int)

points_shape = np_data[:, 1].sum()

points_outcome = 6 * ((np_data[:, 1] - np_data[:, 0] == 1).sum() + (np_data[:, 1] - np_data[:, 0] == -2).sum()) + \
                 3 * ((np_data[:, 1] - np_data[:, 0] == 0).sum())

print(points_shape + points_outcome)

data_adj2 = [str(x).rstrip('\n').replace('A', '1').replace('B', '2').replace('C', '3').replace('X', '0').
             replace('Y', '3').replace('Z', '6').split(' ') for x in data]

np_data2 = np.matrix(data_adj2).astype(int)
points_outcome = np_data2[:, 1].sum()

data_adj3 = [str(x).rstrip('\n').replace('A', '1').replace('B', '2').replace('C', '3').replace('X', '-1').
             replace('Y', '0').replace('Z', '1').split(' ') for x in data]

np_data3 = np.matrix(data_adj3).astype(int)
new_col = np_data3[:, 0] + np_data3[:, 1]
new_col = np.divmod(new_col - 1, 3)[1] + 1
points_shape = new_col.sum()

print(points_shape + points_outcome)
