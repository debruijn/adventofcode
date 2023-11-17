from typing import Union
from util.util import run_day, get_example_data
from aocd import get_data


debug = False


def run_all(example_run: Union[int, bool]):

    if example_run:
        adj_data = get_example_data(2020, 2, example_run-1)
    else:
        data_raw = get_data(day=2, year=2020)
        adj_data = [x for x in data_raw.split('\n')]

    sum_valid1 = 0
    sum_valid2 = 0
    for row in adj_data:
        policy, password = row.split(': ')
        bounds, test_char = policy.split(' ')
        lb, ub = (int(x) for x in bounds.split('-'))
        times = password.count(test_char)
        if lb <= times <= ub:
            sum_valid1 += 1

        if (password[lb-1] == test_char) + (password[ub-1] == test_char) == 1:
            sum_valid2 += 1

    result_part1 = sum_valid1
    result_part2 = sum_valid2

    extra_out = {}
    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
