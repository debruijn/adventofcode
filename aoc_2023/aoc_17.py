from collections import defaultdict
from itertools import product
from typing import Union
from util.util import ProcessInput, run_day
import math

debug = False


def get_next_curr_val(queue):
    curr_val = min(queue.keys(), default=math.inf)
    if curr_val != math.inf and len(queue[curr_val]) == 0:
        del queue[curr_val]
        return get_next_curr_val(queue)
    return curr_val


def run_part(data, lb_turn=0, ub_turn=3):

    data_cmpl = {i + j*1j: int(data[i][j]) for i,j in product(range(len(data)), range(len(data[0])))}

    # Process data
    start = 0 + 0j
    end = len(data) - 1 + (len(data[0])-1)*1j
    start_dirs = [0, 1]  # Two start directions possible
    dir_mapping = {0: 1, 1: 1j, 2: -1, 3: -1j}
    rev_mapping = {1: 0, 1j: 1, -1: 2, -1j: 3}
    best_val = math.inf
    visited = {(start, 0): 0, (start, 1): 0}  # History of visits is relevant across both starting directions
    if debug:
        curr_path = {(start, 0): [start], (start, 1): [start]}

    for curr_dir_nr in start_dirs:
        queue = defaultdict(list)
        queue[0].append((start, curr_dir_nr))
        curr_val = 0
        stop = False

        while not stop:
            # Pop new current location and direction
            curr_loc, curr_dir_nr = queue[curr_val].pop()

            # Based on direction number, construct what are the possible rotations (under restrictions from relevant part)
            this_avail_rots = []
            if curr_dir_nr < 4 * (ub_turn-1):
                this_avail_rots.append(1)
            if curr_dir_nr >= 4 * (lb_turn-1):
                this_avail_rots.extend([1j, -1j])
            curr_dir = dir_mapping[curr_dir_nr % 4]  # Actual direction implied by direction number.

            # For each possible rotation, construct new direction and location
            for rot in this_avail_rots:
                this_dir = curr_dir * rot
                this_loc = curr_loc + this_dir
                outside_area = (this_loc.real < 0 or this_loc.imag < 0 or
                                this_loc.real >= len(data) or this_loc.imag >= len(data[0]))
                if not outside_area:
                    # New direction value: low number if turned, increased number if going straight
                    this_dir_val = rev_mapping[this_dir] if rot != 1 else curr_dir_nr + 4

                    # If we are at endpoint: stop, and see if it's better than what we have
                    if this_loc == end and this_dir_val >= 4 * (lb_turn-1):
                        if curr_val + data_cmpl[end] < best_val:
                            best_val = curr_val + data_cmpl[end]
                            if debug:
                                curr_path[end] = curr_path[(curr_loc, curr_dir_nr)] + [this_loc]
                        stop = True

                    # Not at endpoint: see if we have already been here (loc & dir val), if so, see if this path is better
                    if (this_loc, this_dir_val) not in visited or visited[(this_loc, this_dir_val)] > curr_val + data_cmpl[this_loc]:
                        if (this_loc, this_dir_val) in visited:
                            if (this_loc, this_dir_val) in queue[visited[(this_loc, this_dir_val)]]:
                                queue[visited[(this_loc, this_dir_val)]].remove((this_loc, this_dir_val))  # Remove worse option from Q
                        queue[curr_val + data_cmpl[this_loc]].append((this_loc, this_dir_val))
                        visited[(this_loc, this_dir_val)] = curr_val + data_cmpl[this_loc]
                        if debug:
                            curr_path[(this_loc, this_dir_val)] = curr_path[(curr_loc, curr_dir_nr)] + [(this_loc, this_dir_val, data_cmpl[this_loc])]

            if len(queue[curr_val]) == 0:
                del queue[curr_val]
                curr_val = get_next_curr_val(queue)
                if curr_val >= best_val:
                    stop = True

    if debug:
        print(curr_path[end])

    return best_val


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=17, year=2023).data

    result_part1 = run_part(data, ub_turn=3, lb_turn=0)
    result_part2 = run_part(data, ub_turn=10, lb_turn=4)

    extra_out = {'Dimensions of map in input': (len(data), len(data[0]))}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
