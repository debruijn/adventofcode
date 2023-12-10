from typing import Union
from util.util import ProcessInput, run_day
from math import atan2, pi

debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=10, year=2019).data
    locs = []
    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            if cell == "#":
                locs.append((j, i))

    # select on slope and higher/lower x - don't care about which one is closest
    curr_max = 0
    loc_max = None
    for loc in locs:
        angles = set()
        for other_loc in locs:
            if loc == other_loc:
                pass
            elif loc[0] - other_loc[0] == 0:
                angles.add((loc[1] > other_loc[1], 0))
            else:
                element = 1 if other_loc[0] > loc[0] else -1  # can't be equal, see if-statement
                angles.add((((loc[1] - other_loc[1]) / (loc[0] - other_loc[0])), element))
        curr_max, loc_max = (len(angles), loc) if len(angles) > curr_max else (curr_max, loc_max)
    result_part1 = curr_max

    # find angle (starting at up, clockwise) and distance
    other_locs_per_angle = {}
    for other_loc in locs:
        other_angle = ((-((atan2(-(other_loc[1]-loc_max[1]), other_loc[0]-loc_max[0]) / pi * 180) - 90)) + 360) % 360
        dist = abs(other_loc[1]-loc_max[1]) + abs(other_loc[0]-loc_max[0])
        if other_angle in other_locs_per_angle:
            other_locs_per_angle[other_angle].update({dist: other_loc})
        else:
            other_locs_per_angle[other_angle] = {dist: other_loc}
    assert len(other_locs_per_angle) == result_part1

    # for each angle (sorted), take the lowest distance and remove, until 200 are removed
    keys_sort = sorted(other_locs_per_angle.keys())
    counter = 0
    this_loc = loc_max  # initialize to answer it can't be
    for key in keys_sort:
        if key in other_locs_per_angle:
            this_loc = other_locs_per_angle[key].pop(min(other_locs_per_angle[key].keys()))
            counter += 1
        if counter == 200 if len(data) >= 20 else 10:
            break

    result_part2 = 100 * this_loc[0] + this_loc[1]

    extra_out = {'Dimensions in input': (len(data), len(data[0])),
                 'Loc of maximum': loc_max}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3, 4, 5])
