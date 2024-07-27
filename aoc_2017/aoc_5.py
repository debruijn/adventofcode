from typing import Union
from util.util import ProcessInput, run_day


def do_procedure(data, part_2=False):

    stop = False
    curr_loc = 0
    count_steps = 0
    while not stop:
        old_loc = curr_loc
        curr_loc += data[curr_loc]
        if part_2:
            data[old_loc] = data[old_loc] - 1 if data[old_loc] >= 3 else data[old_loc] + 1
        else:
            data[old_loc] += 1
        if not 0 <= curr_loc < len(data):
            stop = True
        count_steps += 1

    return count_steps


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=5, year=2017).as_int().data

    result_part1 = do_procedure(data.copy())
    result_part2 = do_procedure(data.copy(), part_2=True)

    extra_out = {'Number of entries in input list': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
