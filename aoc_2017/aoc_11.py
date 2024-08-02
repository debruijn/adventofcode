from typing import Union
from util.util import ProcessInput, run_day

# Map direction to coordinates. Main axes: n/s and nw/se. ne = n+se, sw = s+nw
mapping = {'se': 1j, 's': 1, 'n': -1, 'nw': -1j, 'sw': 1-1j, 'ne': 1j-1}


def distance(one, other):
    # Distance between two points in the hexagonal system: since you can reduce distances in both main directions in one
    # step (using the third direction), we can take the max of both differences as the distance.
    return int(max(abs(one.real - other.real), abs(one.imag - other.imag)))


def run_all(example_run: Union[int, bool]):
    # Process data -> split into steps
    data = ProcessInput(example_run=example_run, day=11, year=2017).data
    data = data[0].split(',')

    # Initialize variables
    start = 0 + 0j
    loc = start
    max_dist = 0
    for step in data:
        loc += mapping[step]  # take step
        this_dist = distance(start, loc)  # calculate distance
        max_dist = this_dist if this_dist > max_dist else max_dist  # update max_dist if needed

    result_part1 = distance(start, loc)
    result_part2 = max_dist

    extra_out = {'Number of steps in input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3, 4])
