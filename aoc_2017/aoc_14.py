import operator
from itertools import accumulate
from typing import Union
from util.util import ProcessInput, run_day
from aoc_10 import do_knot_hash_algorithm, batched


def do_knot_hash_64_times(data):
    # For background for this function: see aoc_10.py.
    list_nrs = list(range(256))
    curr_pos, skip_size = 0, 0
    for _ in range(64):
        list_nrs, curr_pos, skip_size = do_knot_hash_algorithm(list_nrs, data, curr_pos, skip_size)
    return list_nrs


def do_aoc_10_in_one_func(subhash):
    # For background for these lines: see aoc_10.py.
    subhash = do_knot_hash_64_times([ord(x) for x in subhash] + [17, 31, 73, 47, 23])
    dense_hash = []
    for sublist in batched(subhash, 16):
        dense_hash.append(list(accumulate(sublist, operator.xor, initial=None))[-1])
    hex_hash = ""
    for element in dense_hash:
        hexed_el = hex(element)[2:]
        hexed_el = "0" + hexed_el if len(hexed_el) == 1 else hexed_el
        hex_hash += hexed_el

    # New part: convert to decimal, then to binary, then to string to remove prefix, and pad with leading 0s with zfill
    bin_hash = "".join([str(bin(int(i, 16))).removeprefix('0b').zfill(4) for i in hex_hash])
    return bin_hash


def run_all(example_run: Union[int, bool]):
    data = ProcessInput(example_run=example_run, day=14, year=2017).data[0]

    # Part 1: create hashes and redo aoc day 10 on each hash to get the grid. Take sum to get result_part1.
    hashes = [data + '-' + str(i) for i in range(128)]
    grid = [[x == '1' for x in do_aoc_10_in_one_func(subhash)] for subhash in hashes]
    result_part1 = sum([sum(row) for row in grid])

    # Part 2: find each region one by one by finding one element, filling the region using BFS, and then remove region
    count_regions = 0
    biggest_region = 0
    while any(any(x for x in row) for row in grid):
        # Find first True in the grid (first the row, then the column)
        find_row = [any(x for x in row) for row in grid].index(True)
        find_col = [x for x in grid[find_row]].index(True)

        # Create region from that element with BFS -> go one step wider if those are bools and not yet included
        queue = [(find_row, find_col)]
        found = []
        while len(queue) > 0:
            this = queue.pop()
            found.append(this)
            for dir in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                new_loc = (this[0] + dir[0], this[1] + dir[1])
                if 0 <= new_loc[0] < 128 and 0 <= new_loc[1] < 128:
                    if grid[new_loc[0]][new_loc[1]] and new_loc not in found:
                        queue.append(new_loc)

        # Convert all elements found to False
        for loc in found:
            grid[loc[0]][loc[1]] = False
        biggest_region = len(found) if len(found) > biggest_region else biggest_region

        # Increase counter by 1
        count_regions += 1

    result_part2 = count_regions

    extra_out = {'Length of string input': len(data),
                 'Biggest region': biggest_region}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
