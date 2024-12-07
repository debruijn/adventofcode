from itertools import product
from math import log10, floor
from typing import Union
from util.util import ProcessInput, run_day
from operator import add, mul


def concat(a, b):
    return a * 10**(floor(log10(b))+1) + b


def get_sum_test_values(data, operators):
    sum_test_values = 0
    for row in data:
        test_value, others = row.split(': ')
        test_value = int(test_value)
        others = [int(x) for x in others.split(' ')]

        for ops in product(operators, repeat=len(others)-1):
            res = others[0]
            for i, op in enumerate(ops):
                res = op(res, others[i+1])
            if res == test_value:
                sum_test_values += test_value
                break
    return sum_test_values


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=7, year=2024).data

    result_part1 = get_sum_test_values(data, [add, mul])
    result_part2 = get_sum_test_values(data, [add, mul, concat])

    extra_out = {'Number of values to check in input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
