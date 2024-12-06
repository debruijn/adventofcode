from typing import Union
from util.util import ProcessInput, run_day


def run_grid(all_locs, obstructions, start, dirn=-1):

    loc = start
    visited_dir = {(loc, dirn)}

    while loc + dirn in all_locs:
        if loc + dirn in obstructions:
            dirn *= -1j
            continue
        if (loc + dirn, dirn) in visited_dir:
            return {}, True
        loc = loc + dirn
        visited_dir.add((loc, dirn))

    return visited_dir, False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=6, year=2024).data

    # Process input into open/obstructions/all lists
    open_locs = set()
    obstructions = set()
    loc = -1
    for i, row in enumerate(data):
        for j, el in enumerate(row):
            if el == '.':
                open_locs.add(i + j*1j)
            elif el == '#':
                obstructions.add(i + j*1j)
            else:
                open_locs.add(i + j*1j)
                loc = i + j*1j
    start_loc = loc
    all_locs = open_locs.union(obstructions)

    # Part 1 path
    initial_path = run_grid(all_locs, obstructions, start_loc)[0]

    loop_locs = set()
    obstr_hist = set()
    for i, (el, dirn) in enumerate(initial_path):
        if el == start_loc or el in obstr_hist:
            continue
        obstr_hist.add(el)
        if run_grid(all_locs, obstructions.union({el}), el - dirn, dirn)[1]:
            loop_locs.add(el)

    result_part1 = len(set(x[0] for x in initial_path))
    result_part2 = len(loop_locs)

    extra_out = {'Dimension of grid': (len(data), len(data[0]))}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
