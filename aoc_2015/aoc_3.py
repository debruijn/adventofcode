from itertools import islice
from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=3, year=2015).data
    mapping = {'>': 1j, '<': -1j, '^': -1, 'v': 1}

    # Part 1
    curr_loc = 0 + 0*1j
    hist = {curr_loc}
    for step in data[0]:
        curr_loc += mapping[step]
        hist.add(curr_loc)
    result_part1 = len(hist)

    # Part 2
    curr_loc = [0 + 0*1j, 0+0*1j]
    hist = set(curr_loc)
    for i in range(0, len(data[0]), 2):
        curr_loc[0] += mapping[data[0][i]]
        hist.add(curr_loc[0])
        if i+1 < len(data[0]):  # Only relevant for 1st example of part 1 applied to part 2
            curr_loc[1] += mapping[data[0][i+1]]
            hist.add(curr_loc[1])
    result_part2 = len(hist)

    extra_out = {'Number of steps in input': len(data[0])}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3])
