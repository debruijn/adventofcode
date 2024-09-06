from itertools import accumulate
from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=1, year=2015).data

    result_part1 = sum(x == '(' for x in data[0]) - sum(x == ')' for x in data[0])
    y = list(accumulate((1 if x == '(' else -1 for x in data[0])))  # Solution to avoid a for loop
    result_part2 = -1 if -1 not in y else y.index(-1) + 1

    extra_out = {'Number of rows in input': len(data[0])}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3, 4, 5, 6, 7, 8, 9])
