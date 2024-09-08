from itertools import pairwise
from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=5, year=2015).data

    # Part 1
    count_nice = 0
    for row in data:
        if sum(row.count(x) for x in 'aeiou') < 3:
            continue
        if not any( x == y for x,y in pairwise(row)):
            continue
        if any(x in row for x in ['ab', 'cd', 'pq', 'xy']):
            continue
        count_nice += 1
    result_part1 = count_nice

    # Part 2
    count_nice = 0
    for row in data:
        pairs = list(pairwise(row))
        if len([x for i, x in enumerate(pairs) if x in pairs[i+2:]]) == 0:
            continue
        if not any(row[i] == row[i+2] for i in range(len(row) - 2)):
            continue
        count_nice += 1
    result_part2 = count_nice

    extra_out = {'Number of strings to test': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3, 4, 5])
