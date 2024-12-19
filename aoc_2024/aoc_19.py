import functools
from typing import Union
from util.util import ProcessInput, run_day


@functools.cache
def design_possible(design, patterns):
    if len(design) == 0:
        return True

    this_possible = False
    for ptrn in patterns:
        if design.startswith(ptrn):
            this_possible = this_possible or design_possible(design[len(ptrn):], patterns)
    return this_possible


@functools.cache
def design_count(design, patterns):
    if len(design) == 0:
        return 1

    this_possible = 0
    for ptrn in patterns:
        if design.startswith(ptrn):
            this_possible += design_count(design[len(ptrn):], patterns)
    return this_possible


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=19, year=2024).as_list_of_strings_per_block().data

    patterns = tuple(data[0][0].split(', '))
    designs = data[1]

    possible_designs, count_designs = 0, 0
    for design in designs:
        possible_designs += 1 if design_possible(design, patterns) else 0
        count_designs += design_count(design, patterns)

    result_part1 = possible_designs
    result_part2 = count_designs

    extra_out = {'Number of patterns in input': len(patterns),
                 'Number of designs in input': len(designs)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
