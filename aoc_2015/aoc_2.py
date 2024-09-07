from itertools import combinations
from math import prod
from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=2, year=2015).data
    paper_to_order = 0
    ribbon_to_order = 0
    for row in data:
        sides = [int(x) for x in row.split('x')]
        sides_surface = [x*y for x,y in combinations(sides, 2)]
        paper_to_order += 2 * sum(sides_surface) + min(sides_surface)
        ribbon_to_order += 2 * (sum(sides) - max(sides)) + prod(sides)

    result_part1 = paper_to_order
    result_part2 = ribbon_to_order

    extra_out = {'Number of presents in input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2])
