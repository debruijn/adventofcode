from collections import defaultdict
from typing import Union
from util.util import ProcessInput, run_day


def get_neighbors(loc):
    return [loc + 1, loc + 1 + 1j, loc + 1j, loc - 1 + 1j, loc - 1, loc - 1 - 1j, loc - 1j, loc + 1 - 1j]


def run_all(example_run: Union[int, bool]):

    input_port = ProcessInput(example_run=example_run, day=3, year=2017).as_single_int().data

    this_step = 1
    num = 1
    while num + 2 * this_step < input_port:
        num += this_step
        num += this_step
        this_step += 1

    coordinate_num = ((this_step-1)//2, (this_step-1)//2)
    if input_port > num + this_step:
        coordinate_port = (coordinate_num[0] - this_step, coordinate_num[1] - (input_port - num - this_step))
    else:
        coordinate_port = (coordinate_num[0] - (input_port - num), coordinate_num[1])

    result_part1 = sum(abs(x) for x in coordinate_port)

    # Bad luck trying to do part 1 in formula form, now I do need to program it in a location-based manner anyway :)
    values = defaultdict(int)
    loc = 0 + 0j
    direction = 1j
    values[loc] = 1
    stop = False
    while not stop:
        loc += direction
        values[loc] = sum(values[x] for x in get_neighbors(loc))
        if values[loc + direction*1j] == 0:
            direction *= 1j
        if values[loc] > input_port:
            stop = True

    result_part2 = values[loc]

    extra_out = {'Input port number': input_port,
                 'Location of part 2 number': f"[{int(loc.real)}, {int(loc.imag)}]"}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3, 4])
