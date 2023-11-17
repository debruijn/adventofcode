import math
from typing import Union
from util.util import ProcessInput, run_day
import numpy as np
import itertools

debug = False


# TODO: optimizible by removing all the iterations that are just there to remove a single 0 (or "x")
# Idea: create offset array that holds the minute differences with the first line for each non-"x" line

def apply_iter_part(num1, diff, num2):
    for i in itertools.count():
        if (num1 * i + diff) % num2 == 0:
            return i


def apply_iter(nums, delay, offset=0):
    return [apply_iter_part(nums[offset], delay[0] - delay[i], nums[i+offset])
            for i in range(1, len(nums)-offset)]


def get_timestamp(nums):
    delay = [-i for i in range(len(nums))]
    answer = 0

    for r in itertools.count():
        delay = apply_iter(nums, delay, r)
        answer += math.prod(nums[:r+1]) * delay[0]
        if len(delay) == 1:
            return answer


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=13, year=2020).as_list_of_ints(pattern=",").data
    minutes_to_wait = [x - (data[0][0] % x) for x in data[1]]
    earliest_bus = np.argmin(minutes_to_wait)
    result_part1 = data[1][earliest_bus] * minutes_to_wait[earliest_bus]

    data = ProcessInput(example_run=example_run, day=13, year=2020).data
    lines = [int(x) if x != 'x' else 1 for x in data[1].split(',')]
    result_part2 = get_timestamp(lines)

    extra_out = {'Number of lines': len(lines),
                 'Number of lines with known number': len([x for x in lines if x > 1])}  # TODO: create dict of additional things to have them printed

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3, 4, 5, 6])
