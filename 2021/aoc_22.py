# Inspired by solution of morgoth1145
# After seeing that my class-based solution would work but would cost me too many hours to refine
# Combining both their solution with what I had made or how I would have programmed his solution in

import numpy as np

with open('aoc_22_data') as f:
    data_raw = f.readlines()

data = [row.replace('\n', '').split(" ") for row in data_raw]
data = np.array(data)
turn_on = data[:, 0]
cuboids = np.array([x.split(',') for x in data[:, 1]])
cuboids = [[x[2:].split('..') for x in y] for y in cuboids]
cuboids = [[range(int(x[0]), int(x[1])+1) for x in y] for y in cuboids]

data = [[turn_on[i]] + cuboids[i] for i in range(len(turn_on))]
part1_dims = [-50, 50]


def get_overlap(this, other):
    if this[-1] < other[0] or this[0] > other[-1]:
        return []
    else:
        return range(max(this[0], other[0]), min(this[-1], other[-1])+1)


def part1(data_f):
    cubes = {}
    for idx, item in enumerate(data_f):
        state, xr, yr, zr = item
        for x in get_overlap(xr, part1_dims):
            for y in get_overlap(yr, part1_dims):
                for z in get_overlap(zr, part1_dims):
                    cubes[x, y, z] = state

    answer = sum(s == 'on' for s in cubes.values())

    print(f'The answer to part one is {answer}')


def count_uninterrupted(item, rest):
    _, xr, yr, zr = item
    total = len(xr) * len(yr) * len(zr)

    conflicts = []

    # For each future item, find overlapping region, add these to conflicts
    for item in rest:
        state, xr2, yr2, zr2 = item

        cxr = get_overlap(xr2, xr)
        cyr = get_overlap(yr2, yr)
        czr = get_overlap(zr2, zr)

        if len(cxr) == 0 or len(cyr) == 0 or len(czr) == 0:
            continue

        conflicts.append((state, cxr, cyr, czr))

    # If there are conflicts, subtract their counts from the current ones
    #  - Because no matter what you do right now, it will be overwritten by a future command
    #  - Take conflicts in the conflicts into account, so rerun this function to do that in negative space
    for idx, item in enumerate(conflicts):
        total -= count_uninterrupted(item, conflicts[idx + 1:])

    return total


def part2(data_f):
    answer = 0
    for idx, item in enumerate(data_f):
        state, xr, yr, zr = item
        if state == 'off':
            continue
        # For each item, add counts but only for those cubes that will not be touched afterwards anymore
        answer += count_uninterrupted(item, data[idx + 1:])

    print(f'The answer to part two is {answer}')


part1(data)
part2(data)
