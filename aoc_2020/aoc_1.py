from typing import Union
from util.util import run_day, get_example_data
import itertools
from aocd import get_data

debug = False


def run_all(example_run: Union[int, bool]):

    if example_run:
        adj_data = get_example_data(2020, 1, example_run - 1)
        adj_data = [int(x) for x in adj_data]
    else:
        data_raw = get_data(day=1, year=2020)
        adj_data = [int(x) for x in data_raw.split('\n')]

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
