import numpy as np

with open('aoc_3_data') as f:
    data = f.readlines()

data = [str(x).rstrip('\n') for x in data]

data_adj = [[int(x) for x in data_x] for data_x in data]
data_np = np.array(data_adj)

most_common = np.median(data_np, axis=0)
least_common = np.array([int(1 - x) for x in most_common])

gamma_rate = np.sum([2**x * np.flip(most_common)[x] for x in range(12)])
epsilon_rate = np.sum([2**x * np.flip(least_common)[x] for x in range(12)])

power = gamma_rate * epsilon_rate
print(power)

## part 2

data_oxygen = np.array(data_adj)
data_co2 = np.array(data_adj)
for i in range(12):
    if data_oxygen.shape[0] > 1:
        most_common = np.ceil(np.median(data_oxygen, axis=0))
        print(most_common)
        data_oxygen = np.array([x for x in data_oxygen if x[i] == int(most_common[i])])
    if data_co2.shape[0] > 1:
        least_common = np.floor(np.array([int(1 - x) for x in np.median(data_co2, axis=0)]))
        print(least_common)
        data_co2 = np.array([x for x in data_co2 if x[i] == int(least_common[i])])

oxygen_rate = np.sum([2**x * np.flip(data_oxygen[0])[x] for x in range(12)])
co2_rate = np.sum([2**x * np.flip(data_co2[0])[x] for x in range(12)])

life_support = oxygen_rate * co2_rate
print(life_support)
