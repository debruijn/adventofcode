import functools
from typing import Union
from util.util import ProcessInput, run_day
from math import lcm

solution = ['naive', 'direct'][1]  # Naive: track each loc; direct: directly check if S would be at top loc
skip = True  # True: only check 2 + 4*i, deducible from "0:3; 1:2" input; False: check all.


def run_all(example_run: Union[int, bool]):

    # Processing: construct firewall dict (depth -> range) and locs_scanner (to track for each range, where is scanner)
    data = ProcessInput(example_run=example_run, day=13, year=2017).replace_substrings(':').as_list_of_ints().data
    firewall = {x[0]: x[1] for x in data}
    locs_scanner = {x: (0, 1) for x in set(firewall.values())}  # In tuple: location and direction

    # Part 1: naive implementation, going through all locations of the scanner after each time step.
    severity = 0
    your_loc = -1
    while your_loc < max(firewall.keys()):
        your_loc += 1
        if your_loc not in firewall:
            pass
        elif locs_scanner[firewall[your_loc]][0] == 0:
            severity += your_loc * firewall[your_loc]
        for k, v in locs_scanner.items():  # Update tuple of location and direction
            locs_scanner[k] = (v[0] + v[1], v[1]) if 0 <= v[0] + v[1] < k else (v[0] - v[1], -v[1])

    result_part1 = severity

    # Part 2: utility functions for naive and direct implementations
    @functools.cache
    def get_loc_dir_after_distance(key, val):  # Used in naive implementation -> caching to skip recalculating
        # location k, length v
        loc = (0, 1)
        for i in range(key):
            loc = (loc[0] + loc[1], loc[1]) if 0 <= loc[0] + loc[1] < val else (loc[0] - loc[1], -loc[1])
        return loc

    def get_loc_with_delay(key, val, delay_f=0):  # Used in naive implementation
        k_star = (key + delay_f) % (2 * (val - 1))
        return get_loc_dir_after_distance(k_star, val)

    def is_zero_with_delay(key, val, delay_f=0):
        return (key + delay_f) % (2 * (val - 1)) == 0

    # Part 2: very extreme upperbound for what the maximum delay could be (after that there is repetition for sure)
    upperbound = lcm(*[2 * (x - 1) for x in locs_scanner.keys()])
    range_inputs = (2, 4) if skip else (0, 1)  # Applying the skip or not
    delay = 0
    if solution == 'direct':
        for delay in range(range_inputs[0], upperbound, range_inputs[1]):
            if not any(is_zero_with_delay(k, v, delay) for k, v in firewall.items()):
                break
    else:
        for delay in range(range_inputs[0], upperbound, range_inputs[1]):
            locs_scanner = {k: get_loc_with_delay(k, v, delay) for k, v in firewall.items()}
            if 0 not in [x[0] for x in locs_scanner.values()]:
                break

    result_part2 = delay

    extra_out = {'Number of rows in input': len(data),
                 'Firewall depth': max(firewall.keys()),
                 'Maximum range': max(firewall.values()),
                 'Absolute upperbound using LCM': upperbound}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
