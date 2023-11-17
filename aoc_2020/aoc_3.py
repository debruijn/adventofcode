from typing import Union
from util.util import run_day, get_example_data
from aocd import get_data


debug = False


def check_slope(data, offset_x, offset_y):

    curr_loc = 0
    sum_trees = 0
    for row in data[offset_y:len(data):offset_y]:
        curr_loc += offset_x
        if curr_loc >= len(row):
            curr_loc -= len(row)
        if row[curr_loc] == '#':
            sum_trees += 1
    return sum_trees


def run_all(example_run: Union[int, bool]):

    if example_run:
        adj_data = get_example_data(2020, 3, example_run-1)
    else:
        data_raw = get_data(day=3, year=2020)
        adj_data = [x for x in data_raw.split('\n')]

    curr_loc = 0
    sum_trees = 0
    for row in adj_data[1:]:
        curr_loc += 3
        if curr_loc >= len(row):
            curr_loc -= len(row)
        if row[curr_loc] == '#':
            sum_trees += 1

    result_part1 = check_slope(adj_data, 3, 1)
    result_part2 = result_part1 * check_slope(adj_data, 1, 1)
    result_part2 *= check_slope(adj_data, 5, 1)
    result_part2 *= check_slope(adj_data, 7, 1)
    result_part2 *= check_slope(adj_data, 1, 2)

    extra_out = {}
    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
