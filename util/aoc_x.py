from typing import Union
from util.util import timing, ProcessInput, run_day

debug = False


@timing
def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=None).as_int()

    result_part1 = "TODO"
    result_part2 = "TODO"

    extra_out = None  # TODO: create dict of additional things to have them printed

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
