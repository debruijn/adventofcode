from functools import cache
from typing import Union
from util.util import ProcessInput, run_day


# Function to find whether num is wall or not. Makes use of caching to avoid recalculating.
@cache
def is_open(loc, fav_num):
    if loc.imag < 0 or loc.real < 0:
        return False
    raw_num = int(loc.real**2 + 3*loc.real + 2*loc.real*loc.imag + loc.imag + loc.imag**2 + fav_num)
    count_1s = bin(raw_num).count('1')
    return (count_1s % 2) == 0


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=13, year=2016).data

    # Initialize variables: starting location and nr_steps, queue and history for BFS, designer's favorite number
    loc = 1 + 1j
    this_steps = 0
    queue = [(loc, this_steps)]
    hist = [loc]
    fav_num = int(data[0])

    # More initialization: target location (part 1) and target number of steps (part 2) and related variables
    target = 7 + 4j if example_run else 31 + 39j
    num_steps = 10 if example_run else 50
    not_at_num_steps = True
    nr_reachable_at_num_steps = -1

    while len(queue) > 0:
        this_loc, this_steps = queue.pop(0)
        if this_steps > num_steps and not_at_num_steps:  # Part 2
            not_at_num_steps = False
            nr_reachable_at_num_steps = len(set(hist))  # Set to avoid duplicates (without doing a conditional append)

        hist.append(this_loc)
        if this_loc == target:  # Part 1
            break

        for step in (1, -1, 1j, -1j):
            if this_loc+step in hist:
                continue
            if is_open(this_loc+step, fav_num):
                queue.append((this_loc+step, this_steps+1))

    result_part1 = this_steps
    result_part2 = nr_reachable_at_num_steps

    extra_out = {'Designer\'s favorite number': fav_num,
                 'Length of history when target is found': len(set(hist)),
                 'Point visited that is furthest away': str(max(hist, key=lambda x: abs(x))).
                 replace('+', ',').replace('j)', '').replace('(', '')}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
