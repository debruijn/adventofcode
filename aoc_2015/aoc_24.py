from itertools import combinations
from math import prod
from typing import Union
from util.util import ProcessInput, run_day


def do_balancing(data, k=3):

    target_weight = sum(data) // k
    curr_size = target_weight // max(data)  # Skip lower sizes -> round down so I can take a "+1" in the while loop

    smallest_nr = []
    while len(smallest_nr) == 0:
        curr_size += 1
        for these in combinations(data, curr_size):
            if sum(these) != target_weight:
                continue
            # others = [x for x in data if x not in these]  <-- Technically should check if these are equally divisible
            smallest_nr.append(these)

    return prod(min(smallest_nr, key=prod))  # Find lowest QE


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=24, year=2015).as_int().data

    result_part1 = do_balancing(data, k=3)
    result_part2 = do_balancing(data, k=4)

    extra_out = {'Number of packages': len(data),
                 'Weight per compartment for both parts': (sum(data)//3, sum(data)//4)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
