from itertools import product
from typing import Union
from util.util import ProcessInput, run_day

debug = False


def get_area(path):
    loc = 0 + 0j
    outer_line = 0
    inner_area = 0
    for this_dir, this_length in path:
        this_step = this_dir * this_length
        loc += this_dir * this_length
        inner_area += loc.real * this_step.imag
        outer_line += this_length
    total_area = abs(inner_area) + abs(int(outer_line/2)) + 1

    return int(abs(inner_area)), int(outer_line), int(total_area)


## THIS METHOD IS NOT USED FOR THE SOLVE RIGHT NOW - IT ONLY WORKS FOR PART A ##
def solve_via_fill_algorithm(data, dir_mapping):
    loc = 0 + 0j
    visited = {loc}
    min_i, min_j, max_i, max_j = 0, 0, 0, 0

    # Convert instructions into which cells have been visited
    all_hex = []
    for row in data:
        this_dir, this_length, this_hex = row.split(' ')
        all_hex.append(this_hex.replace('(', '').replace(')', '').replace('#', ''))
        for i in range(int(this_length)):
            loc += dir_mapping[this_dir]
            visited.add(loc)
            if loc.real < min_i:
                min_i = int(loc.real)
            if loc.real > max_i:
                max_i = int(loc.real)
            if loc.imag < min_j:
                min_j = int(loc.imag)
            if loc.imag > max_j:
                max_j = int(loc.imag)

    if debug:  # plot of structure
        for i in range(min_i, max_i + 1):
            this_str = ""
            for j in range(min_j, max_j + 1):
                this_str += '#' if i + j * 1j in visited else ' '
            print(this_str)

    # Outside fill algorithm: initialization
    unchecked = set([i + j * 1j for i, j in product(range(min_i - 1, max_i + 2), range(min_j - 1, max_j + 2))])
    unchecked = unchecked.difference(visited)
    queue = [max_i + min_j * 1j]
    outside = []

    # Outside fill algorithm: execution of it
    while len(queue) > 0:
        curr_loc = queue.pop()
        outside.append(curr_loc)
        for this_dir in [1, 1j, -1, -1j]:
            this_loc = curr_loc + this_dir
            if this_loc in unchecked:
                queue.append(this_loc)
                unchecked.remove(this_loc)

    return len(unchecked) + len(visited)


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=18, year=2023).data
    dir_mapping = {'R': 1j, 'D': 1, 'L': -1j, 'U': -1}

    # Part 1
    instr = [(dir_mapping[x.split()[0]], int(x.split()[1])) for x in data]
    result_part1 = get_area(instr)[2]  #  solve_via_fill_algorithm(data, dir_mapping)

    # Part 2
    decode_dir = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}
    all_hex = [row.split(' ')[2].replace('(', '').replace(')', '').replace('#', '') for row in data]
    true_instr = [(dir_mapping[decode_dir[x[5]]], int(x[:5], 16)) for x in all_hex]
    result_part2 = get_area(true_instr)[2]

    extra_out = {'Number of instructions in input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
