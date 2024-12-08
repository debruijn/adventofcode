from collections import defaultdict
from itertools import combinations
from typing import Union
from util.util import ProcessInput, run_day


def check_loc(pt, dims):
    return pt.real >= 0 and pt.imag >= 0 and pt.real < dims[0] and pt.imag < dims[1]


def find_antinodes(antennas, dims, try_range):
    # Find all antinodes by trying multiples of the difference vector. Currently, as multiplier of the diff vector, all
    # values between -gridsize and gridsize are tried, to account for the smallest diff vector. This is of course very
    # inefficient but already below 0.03s in Python so that's fine for me.
    # To improve: split into a plus and minor range (so 0 to K and 0 to -K instead of -K to K), and break when the new
    # pt is not within bounds.
    antinode_locs = set()
    for ant_type in antennas.keys():
        for pt1, pt2 in combinations(antennas[ant_type], 2):
            for mult in try_range:
                new_pt1, new_pt2 = pt1 - mult*(pt2 - pt1), pt2 - mult*(pt1 - pt2)
                if check_loc(new_pt1, dims):
                    antinode_locs.add(new_pt1)
                if check_loc(new_pt2, dims):
                    antinode_locs.add(new_pt2)

    return len(antinode_locs)

def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=8, year=2024).data

    antennas = defaultdict(list)
    for i, row in enumerate(data):
        for j, el, in enumerate(row):
            if el != '.':
                antennas[el].append(i + j*1j)

    dims = [len(data), len(data[0])]

    result_part1 = find_antinodes(antennas, dims, [-2, 1])
    result_part2 = find_antinodes(antennas, dims, range(-max(dims), max(dims)+1))

    extra_out = {'Size of grid in input': (len(data), len(data[0])),
                 'Number of antenna types': len(antennas.keys())}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
