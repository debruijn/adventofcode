from itertools import combinations
from math import prod
from typing import Union
from util.util import ProcessInput, run_day


def do_balancing(data, k=3, skip_check=False):

    target_weight = sum(data) // k
    curr_size = target_weight // max(data)  # Skip lower sizes -> round down so I can take a "+1" in the while loop
    max_size = len(data) // k

    smallest_nr = []
    while len(smallest_nr) == 0:
        curr_size += 1
        if curr_size > max_size:
            return False
        for these in combinations(data, curr_size):
            if sum(these) != target_weight:
                continue
            if not skip_check:
                others = [x for x in data if x not in these]  # Those not in group 1 should also be divisible
                if k == 2:
                    return True  # Next k would be 1, and you can always evenly split items into 1 group.
                if not do_balancing(others, k=k-1):
                    continue
            smallest_nr.append(these)

    return prod(min(smallest_nr, key=prod))  # Find lowest QE


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=24, year=2015).as_int().data

    # Set skip_check=False to True to speed-up solution, without validation that the other groups can be evenly split.
    result_part1 = do_balancing(data, k=3, skip_check=False)
    result_part2 = do_balancing(data, k=4, skip_check=False)

    extra_out = {'Number of packages': len(data),
                 'Weight per compartment for both parts': (sum(data)//3, sum(data)//4)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
