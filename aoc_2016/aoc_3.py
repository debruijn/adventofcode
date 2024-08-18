from itertools import islice
from typing import Union
from util.util import ProcessInput, run_day


def batched(iterable, n):
    # batched('ABCDEFG', 3) → ABC DEF G
    # From Python 3.12 documentation
    iterator = iter(iterable)
    while batch := tuple(islice(iterator, n)):
        yield batch


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=3, year=2016).as_list_of_ints().data

    # Part 1: directly sorting and then comparing the numbers, as instructed
    count_valid = 0
    for row in data:
        row = sorted(row)
        if row[0] + row[1] > row[2]:
            count_valid += 1
    result_part1 = count_valid

    # Part 2: flipping each three rows to be columns, and then repeat part 1 on those
    count_valid = 0
    if not example_run:
        for rows in batched(data, n=3):
            rows = [[x[i] for x in rows] for i in range(3)]
            for row in rows:
                row = sorted(row)
                if row[0] + row[1] > row[2]:
                    count_valid += 1
    result_part2 = count_valid

    extra_out = {'Number of potential triangles to check': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
