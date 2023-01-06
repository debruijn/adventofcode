import numpy as np

with open('aoc_3_data') as f:
    data = f.readlines()

adj_data = [row.rstrip('\n') for row in data]
len_data = [len(row) for row in adj_data]
half_len_data = [int(len_nr/2) for len_nr in len_data]

sum_priority = 0
for i in range(len(adj_data)):
    half_1 = set(adj_data[i][0:half_len_data[i]])
    half_2 = set(adj_data[i][half_len_data[i]:len_data[i]])
    overlap = list(half_1.intersection(half_2))[0]
    if overlap.islower():
        priority = ord(overlap) - ord('a') + 1
    else:
        priority = ord(overlap) - ord('A') + 27

    sum_priority += priority

print(sum_priority)


adj_data = [row.rstrip('\n') for row in data]

sum_priority = 0
for i in range(int(len(adj_data)/3)):
    i1 = 3*i
    i2 = 3*i+1
    i3 = 3*i+2

    set1 = set(adj_data[i1])
    set2 = set(adj_data[i2])
    set3 = set(adj_data[i3])
    overlap = list(set1.intersection(set2).intersection(set3))[0]
    if overlap.islower():
        priority = ord(overlap) - ord('a') + 1
    else:
        priority = ord(overlap) - ord('A') + 27

    sum_priority += priority

print(sum_priority)
