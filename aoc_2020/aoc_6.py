from typing import Union
from util.util import timing, run_day


debug = False


def run_all(example_run: Union[int, bool]):

    file = f'aoc_6_exampledata{example_run}' if example_run else 'aoc_6_data'
    with open(file) as f:
        data = f.readlines()
    adj_data = [row.rstrip('\n') for row in data]

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

