from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=4, year=2025).data

    locs = []
    for i, row in enumerate(data):
        for j, el in enumerate(row):
            if el == '@':
                locs.append(i + j*1j)

    dirs = [1, 1+1j, 1j, -1 + 1j, -1, -1-1j, -1j, 1-1j]

    nr_accessible = 0
    for pt in locs:
        count = sum([1 for _dir in dirs if pt + _dir in locs])
        if count < 4:
            nr_accessible +=1

    result_part1 = nr_accessible

    nr_removed = 0
    last_removed = -1
    while nr_removed != last_removed:
        last_removed = nr_removed
        for pt in locs:
            count = sum([1 for _dir in dirs if pt + _dir in locs])
            if count < 4:
                nr_removed +=1
                locs.remove(pt)

    result_part2 = nr_removed

    extra_out = {'Number of rows in input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
