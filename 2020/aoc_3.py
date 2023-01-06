from typing import Union
from util import timing


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


@timing
def run_all(example_run: Union[int, bool]):

    file = f'aoc_3_exampledata{example_run}' if example_run else 'aoc_3_data'
    with open(file) as f:
        data = f.readlines()
    adj_data = [row.rstrip('\n') for row in data]
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

    print(f'\nResults for {f"example" if example_run else "my"} input{f" {example_run}" if example_run else ""}:')
    print(f' Result of part 1: {result_part1}')
    print(f' Result of part 2: {result_part2}')


if __name__ == "__main__":
    [run_all(example_run=i) for i in [1]]
    run_all(example_run=False)
