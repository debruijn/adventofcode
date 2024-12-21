import functools
from typing import Union
from util.util import ProcessInput, run_day


# Numpad and directional pad grids, starts and locs
grid1 = {0: '7', 1: '4', 2: '1', 0 + 1j: '8', 1 + 1j: '5', 2 + 1j: '2', 3 + 1j: '0', 0 + 2j: '9', 1 + 2j: '6',
         2 + 2j: '3', 3 + 2j: 0}
start1 = 3 + 2j
locs1 = {v: k for k, v in grid1.items()}
grid2 = {1: -1j, 1j: -1, 1 + 1j: 1, 1 + 2j: 1j, 2j: 0}
start2 = 2j
locs2 = {v: k for k, v in grid2.items()}


@functools.cache
def path_cost(path, level, max_lvl):
    if level == max_lvl:  # Human giving instructions, so just sum(manhattan_dist + 1) for each button (+1 for A)
        loc = start2
        dist = 0
        for pth in path:
            pth_loc = locs2[pth]
            dist += abs(pth_loc.imag - loc.imag) + abs(pth_loc.real - loc.real) + 1
            loc = pth_loc
        return int(dist)
    else:  # Robot giving instructions to robot, so the number of steps needs to be "thrown upwards" to the next level
        loc = start2 if level > 0 else start1
        dist = 0
        for pth in path:
            pth_loc = locs2[pth] if level > 0 else locs1[pth]
            diff_loc = pth_loc - loc

            # Horizontal and vertical steps - ignoring the weird corner case
            hor = (1j,) * int(abs(diff_loc.imag)) if diff_loc.imag >= 0 else (-1j,) * int(abs(diff_loc.imag))
            vert = (1,) * int(abs(diff_loc.real)) if diff_loc.real >= 0 else (-1,) * int(abs(diff_loc.real))

            # Priority: left > down > other two if possible, but test if corner gets in the way of that
            if diff_loc.imag < 0 and pth_loc.imag*1j + loc.real in (grid2 if level > 0 else grid1):
                this_path = hor + vert + (0,)
            elif loc.imag*1j + pth_loc.real in (grid2 if level > 0 else grid1):
                this_path = vert + hor + (0,)
            else:
                this_path = hor + vert + (0,)

            dist += path_cost(this_path, level + 1, max_lvl)  # What does it cost to do this_path for next robot?
            loc = pth_loc
        return int(dist)


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=21, year=2024).data

    total_complexity = 0
    for code in data:
        code = tuple(x if x!='A' else 0 for x in code)
        len_code = path_cost(code, 0, 2)
        total_complexity += len_code * int("".join(code[:-1]))
    result_part1 = total_complexity

    total_complexity = 0
    for code in data:
        code = tuple(x if x!='A' else 0 for x in code)
        len_code = path_cost(code, 0, 25)
        total_complexity += len_code * int("".join(code[:-1]))
    result_part2 = total_complexity

    extra_out = {'Number of codes in input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
