from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=4, year=2025).data
    lens = len(data), len(data[0])
    data = [[y for y in x] for x in data]

    locs = []
    for i, row in enumerate(data):
        for j, el in enumerate(row):
            if el == '@':
                locs.append(i + j*1j)

    nr_accessible = 0
    for pt in locs:
        x, y = int(pt.real), int(pt.imag)
        if data[x][y] == ".":
            continue
        count = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if x + i < 0 or x + i >= lens[0] or y + j < 0 or y + j >= lens[1]:
                    continue
                if data[x + i][y + j] == '@':
                    count += 1
        if count < 5:
            nr_accessible += 1

    result_part1 = nr_accessible

    nr_removed = 0
    last_removed = -1
    while nr_removed != last_removed:
        last_removed = nr_removed
        for pt in locs:
            x, y = int(pt.real), int(pt.imag)
            if data[x][y] == ".":
                continue
            count = 0
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if x+i < 0 or x+i >= lens[0] or y+j < 0 or y+j >= lens[1]:
                        continue
                    if data[x + i][y + j] == '@':
                        count +=1
            if count < 5:
                nr_removed += 1
                data[x][y] = "."

    result_part2 = nr_removed

    extra_out = {'Dimension of input': lens}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
