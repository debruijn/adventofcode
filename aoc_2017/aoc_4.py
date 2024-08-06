from itertools import combinations
from typing import Union
from util.util import ProcessInput, run_day
from collections import Counter


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=4, year=2017).data

    result_part1 = sum(len(set(row.split())) == len(row.split()) for row in data)

    # Initial setup of part 2
    # sum_valid = 0
    # for row in data:
    #     this_row = [Counter(x) for x in row.split()]
    #     unique = True
    #     for i, j in combinations(this_row, 2):
    #         if i == j:
    #             unique = False
    #     sum_valid += unique

    sum_valid = 0
    for row in data:
        this_row = [Counter(x) for x in row.split()]  # Converting to Counter removes the order
        sum_valid += all([i != j for i, j in combinations(this_row, 2)])

    result_part2 = sum_valid

    extra_out = {'Number of potential passphrases in input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3])  # 388 too high
