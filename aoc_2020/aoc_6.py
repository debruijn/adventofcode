from typing import Union
from util.util import run_day, get_example_data
from aocd import get_data


debug = False


def run_all(example_run: Union[int, bool]):

    if example_run:
        adj_data = get_example_data(2020, 6, example_run-1)
    else:
        data_raw = get_data(day=6, year=2020)
        adj_data = [x for x in data_raw.split('\n')]

    curr_set = set()
    sum_count = 0
    for row in adj_data:
        if row == "":
            sum_count += len(curr_set)
            curr_set = set()
        else:
            curr_set = curr_set.union(set(row))
    result_part1 = sum_count + len(curr_set)

    curr_set = False
    sum_count = 0
    for row in adj_data:
        if row == "":
            sum_count += len(curr_set)
            curr_set = False
        else:
            if curr_set == False:
                curr_set = set(row)
            else:
                curr_set = curr_set.intersection(set(row))
    result_part2 = sum_count + len(curr_set)

    extra_out = {}
    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])

