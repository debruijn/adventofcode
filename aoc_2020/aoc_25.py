from typing import Union
from util.util import ProcessInput, run_day

debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=25, year=2020).as_int().data

    val = 1
    loop = 0
    subject_nr = 7
    div_value = 20201227
    while val not in data:
        val = (val * subject_nr) % div_value
        loop += 1

    new_val = 1
    for i in range(loop):
        if val == data[0]:
            new_val = (new_val * data[1]) % div_value
        else:
            new_val = (new_val * data[0]) % div_value

    result_part1 = new_val
    result_part2 = "Merry Christmas"

    extra_out = {'Number of keys in input': len(data)}  # TODO: create dict of additional things to have them printed

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
