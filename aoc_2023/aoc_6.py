from typing import Union
from util.util import ProcessInput, run_day
from functools import reduce
from operator import mul

debug = False
method = ["naive_method", "optimized_method"][1]
print(f'Running this script using the method: {method}')

# This script contains a naive and an optimized method. The optimization is applied in the sense of: no checking of what
# is not needed to check - needs concave & symmetric function (which we have in this problem).
# It starts at middle point and expands until it doesn't meet distance requirement anymore

# Further optimizations:
# - Make bigger jumps initially and zoom in on smaller jumps when requirement is not valid
# - The above but go in both directions (does not assume symmetric function)
# - Use a different search function (binary search, etc) (can depend on symmetry, depending on implementation)
# - Solve it mathematically, it is a parabola :) -> not interesting from a programming perspective though!


def naive_method(time, distance):
    n_combinations = 0
    for i in range(time):
        n_combinations += 1 if i * (time - i) > distance else 0
    return n_combinations


def optimized_method(time, distance):
    still_winning = True
    i = int(time / 2)  # midpoint
    n_combinations = 1 if 2 * i == time else 2  # differentiates between odd and even time
    while still_winning:
        i = i - 1
        if i * (time - i) > distance:
            n_combinations += 2  # function is symmetric, so we go down from i_max but count i>i_max as well
        else:
            still_winning = False
    return n_combinations


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=6, year=2023).data
    method_f = globals()[method]

    # Part 1
    time_1 = [int(x.strip()) for x in data[0].split()[1:]]
    distance_1 = [int(x.strip()) for x in data[1].split()[1:]]
    result_part1 = reduce(mul, (method_f(t, d) for t,d in zip(time_1, distance_1)), initial=1)

    # # Part 2
    time_2 = int(data[0].split(':')[1].replace(' ', ''))
    distance_2 = int(data[1].split(':')[1].replace(' ', ''))
    result_part2 = method_f(time_2, distance_2)

    extra_out = {'Number of initial races in input': len(time_1),
                 'Total time for actual race': time_2}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
