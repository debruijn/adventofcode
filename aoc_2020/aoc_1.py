from typing import Union
from util.util import run_day
import itertools


debug = False


def run_all(example_run: Union[int, bool]):

    file = f'aoc_1_exampledata{example_run}' if example_run else 'aoc_1_data'
    with open(file) as f:
        data = f.readlines()
    adj_data = [int(row.rstrip('\n')) for row in data]

    result_part1 = "TODO"
    result_part2 = "TODO"

    for x, y in itertools.combinations(adj_data, 2):
        if x + y == 2020:
            result_part1 = x * y

    for x, y, z in itertools.combinations(adj_data, 3):
        if x + y + z == 2020:
            result_part2 = x * y * z

    extra_out = {}
    return result_part1, result_part2, extra_out

if __name__ == "__main__":
    run_day(run_all, [1])
