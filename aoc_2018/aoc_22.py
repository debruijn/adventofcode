from collections import defaultdict
from typing import Union
from util.util import ProcessInput, run_day
from functools import cache

debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=22, year=2018).data

    # Processing input
    depth = int(data[0].split(' ')[1])
    target = tuple(int(x) for x in data[1].split(' ')[1].split(','))
    mouth = (0, 0)

    def get_geologic(coordinates):
        if coordinates in [mouth, target]:
            return 0
        if coordinates[1] == 0:
            return coordinates[0] * 16807
        if coordinates[0] == 0:
            return coordinates[1] * 48271
        return get_erosion((coordinates[0] - 1, coordinates[1])) * get_erosion((coordinates[0], coordinates[1] - 1))

    @cache
    def get_erosion(coordinates):
        return (get_geologic(coordinates) + depth) % 20183

    # Part 1: use functions above to find risk levels
    risk_level = 0
    for j in range(target[1]+1):
        str_cave = ""
        for i in range(target[0]+1):
            risk_level += get_erosion((i, j)) % 3
            if debug:
                if (i, j) == mouth:
                    str_cave += 'M'
                elif (i, j) == target:
                    str_cave += 'T'
                elif get_erosion((i, j)) % 3 == 0:
                    str_cave += '.'
                elif get_erosion((i, j)) % 3 == 1:
                    str_cave += '='
                elif get_erosion((i, j)) % 3 == 2:
                    str_cave += '|'
        if debug:
            print(str_cave)

    # Part 2: see what locations we can reach with what tool equipped by time t, and keep increasing t until at target.
    queue = defaultdict(list)
    t = 0
    queue[t].append((mouth, 1))  # nr of tool := what is not allowed - so starting with Torch is 1 since Wet is 1 above
    hist = dict()
    while True:
        # Pop next state (location/tool)
        if len(queue[t]) == 0:
            if debug:
                print(t, len(hist), len(queue[t + 1]))
            t += 1
            continue
        curr_loc, curr_tool = queue[t].pop()

        if curr_loc == target and curr_tool == 1:
            break  # If we are there with the right tool, we can stop

        # If we were already on this location with this tool before, skip this iteration
        if (curr_loc, curr_tool) in hist:
            continue
        hist[(curr_loc, curr_tool)] = t

        # Type 1 of new candidates: set a step with current tool equipped, if that is allowed
        for step in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            new_loc = (curr_loc[0] + step[0], curr_loc[1] + step[1])
            if new_loc[0] >= 0 and new_loc[1] >= 0:
                if get_erosion(new_loc) % 3 != curr_tool:
                    new_state = (new_loc, curr_tool)
                    if new_state not in hist:
                        queue[t + 1].append(new_state)

        # Type 2 of new candidates: swap out tool, if that is allowed here
        for other_tool in [x for x in (0, 1, 2) if x != curr_tool]:
            if get_erosion(curr_loc) % 3 != other_tool:
                new_state = (curr_loc, other_tool)
                if new_state not in hist:
                    queue[t + 7].append(new_state)

    result_part1 = risk_level
    result_part2 = t

    extra_out = {'Target loc': target,
                 'Number of states considered': len(hist)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
