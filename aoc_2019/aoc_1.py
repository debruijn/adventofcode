from typing import Union
from util.util import ProcessInput, run_day

debug = False


def fuel(x, recursive=False):
    answer = divmod(x, 3)[0] - 2
    return 0 if answer <= 0 else answer + fuel(answer, True) if recursive else answer


def run_all(example_run: Union[int, bool]):

    mass = ProcessInput(example_run=example_run, day=1, year=2019).as_int().data

    result_part1 = sum([fuel(x, recursive=False) for x in mass])
    result_part2 = sum([fuel(x, recursive=True) for x in mass])

    extra_out = {}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3, 4])
