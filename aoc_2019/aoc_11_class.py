from collections import defaultdict
from typing import Union
from util.util import ProcessInput, run_day
from intcode_pc import IntCodePC


debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=11, year=2019).as_list_of_ints(pattern=',').data[0]

    field = defaultdict(lambda: 0)
    loc = 0 + 0j
    dir = 0 + 1j
    next_out_is_dir = False

    PC = IntCodePC(data, [field[loc]])
    stop = False
    while not stop == 1:
        out, stop = PC.run_until_output([field[loc]])
        if stop == 2:
            if next_out_is_dir:
                dir *= -1j if out[0] == 1 else 1j
                loc += dir
            else:
                field[loc] = out[0]
            next_out_is_dir = not next_out_is_dir
            PC.clean_out()

    result_part1 = len(field)

    field = defaultdict(lambda: 0)
    loc = 0 + 0j
    dir = 0 + 1j
    next_out_is_dir = False
    field[loc] = 1

    PC = IntCodePC(data, [field[loc]])
    stop = False
    while not stop == 1:
        out, stop = PC.run_until_output([field[loc]])
        if stop == 2:
            if next_out_is_dir:
                dir *= -1j if out[0] == 1 else 1j
                loc += dir
            else:
                field[loc] = out[0]
            next_out_is_dir = not next_out_is_dir
            PC.clean_out()

    range_x = range(int(min([x.real for x in field.keys()])), int(max([x.real for x in field.keys()]) + 1))
    range_y = range(int(max([x.imag for x in field.keys()])), int(min([x.imag for x in field.keys()]) - 1), -1)
    for y in range_y:
        this_line = ""
        for x in range_x:
            this_line += "#" if field[x + y*1j] == 1 else " "
        print(this_line)

    result_part2 = "HGEHJHUZ"

    extra_out = {'Answer of part 1 if applied to start value of part 2': len(field),
                 'Actually filled in values in part 2': sum(field.values())}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [])
