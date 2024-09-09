from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=8, year=2015).data

    nr_literal, nr_memory, nr_expanded = 0, 0, 0
    for row in data:
        nr_literal += len(row)
        nr_memory += len(eval(row))
        nr_expanded += len(row) + sum(row.count(x) for x in '"\\') + 2

    result_part1 = nr_literal - nr_memory
    result_part2 = nr_expanded - nr_literal

    extra_out = {'Number of strings in input': len(data),
                 'Number of literal characters': nr_literal,
                 'Number of characters in memory': nr_memory,
                 'Expanded string total length': nr_expanded}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
