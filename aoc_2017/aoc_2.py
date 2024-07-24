from itertools import product
from typing import Union
from util.util import ProcessInput, run_day

debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=2, year=2017).as_list_of_ints(" " if example_run else "\t").data

    checksum = 0
    for row in data:
        checksum += max(row) - min(row)
    result_part1 = checksum

    sum_evenly_divisible = 0
    for row in data:
        sum_evenly_divisible += sum([i//j for i, j in product(row, repeat=2) if i/j == i//j and i != j])
        if debug:
            [print(i, j, i//j, row) for i, j in product(row, repeat=2) if i / j == i // j and i != j]
    result_part2 = sum_evenly_divisible

    extra_out = {'Number of rows in input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
