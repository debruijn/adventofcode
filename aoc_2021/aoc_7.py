import numpy as np

with open('aoc_7_data') as f:
    data = f.readlines()

data = np.array([int(x) for x in data[0].replace('\n', '').split(',')])

part = 2


def single_cost(diff, part=2):
    if part == 1:
        return diff
    else:
        return (diff + 1) * diff / 2  # Part 1: just diff


def fuel_cost(pos, data_f):
    return np.sum(single_cost(np.abs(data_f - pos), part=part))


candidate = np.median(data) if part == 1 else np.round(np.mean(data))
stop = False
while not stop:
    if ((fuel_cost(candidate, data) < fuel_cost(candidate - 1, data)) and
            (fuel_cost(candidate, data) < fuel_cost(candidate + 1, data))):
        stop = True
    else:
        candidate = candidate + 1 if fuel_cost(candidate + 1, data) < fuel_cost(candidate - 1, data) else candidate - 1
    print(f"Candidate: {candidate}, fuel: {fuel_cost(candidate, data)}")

print(f"Solution: {candidate}, fuel: {fuel_cost(candidate, data)}")
