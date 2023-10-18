from typing import Union
from util.util import run_day


debug = False


def run_all(example_run: Union[int, bool]):

    file = f'aoc_2_exampledata{example_run}' if example_run else 'aoc_2_data'
    with open(file) as f:
        data = f.readlines()
    adj_data = [row.rstrip('\n') for row in data]

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
