from collections import defaultdict
from typing import Union
from util.util import ProcessInput, run_day


def do_algorithm(data, N, st=2):
    # Overall approach: keep track of the infection stage for each non-clean node, and update loc/dir accordingly.

    # Initialize location, direction and counter (using complex numbers for location and direction)
    curr_loc = len(data)//2 + len(data[0])//2 * 1j
    curr_dir = -1
    count_infections = 0

    # Map input to a list of infected, using complex numbers to map to a location
    infected = [i + j*1j for i, row in enumerate(data) for j, col in enumerate(row) if col == '#']
    infection_stage = defaultdict(int)
    infection_stage.update({x: 2 for x in infected})

    # Mapping of how to update direction based on infection stage
    stage_dir_mapping = {0: 1j, 1: 1, 2: -1j, 3: -1}
    for i in range(N):
        curr_dir *= stage_dir_mapping[infection_stage[curr_loc]]
        infection_stage[curr_loc] += st
        if infection_stage[curr_loc] == 2:
            count_infections += 1
        elif infection_stage[curr_loc] == 4:
            del infection_stage[curr_loc]  # Clean up of clean nodes, to keep the dict small as possible
        curr_loc += curr_dir

    return count_infections


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=22, year=2017).data

    result_part1 = do_algorithm(data, 10000, 2)
    result_part2 = do_algorithm(data, 10000000, 1)

    extra_out = {'Size of both dimensions in starting grid in input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
