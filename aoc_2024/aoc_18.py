import math
from collections import defaultdict
from itertools import product, count
from typing import Union
from util.util import ProcessInput, run_day


# Current implementation for part 2:
# - Start from having all bytes in there, and keep removing one until there is a path (-> failed paths are faster)
# - Still takes 20seconds though..

# Some routes to improvement of run time of part 2:
# - Binary search -> this means the algo will still need to run a couple of times
# - Keep memory of path and if new byte is not on path, skip -> this means the algo will still run plenty of times
# - Good old "Do it in Rust without improving the algorithm"
# - Improving speed of algorithm itself -> gain for each run
#   - Not using "free" spaces but instead adding the blocked ones to hist already (and checking "free" using dimensions)


def run_algo_dfs(free, loc, target):

    queue = [(loc, 0)]
    hist = defaultdict(lambda: math.inf)
    hist[loc] = 0

    while len(queue) > 0:
        loc, steps = queue.pop()

        if loc == target and steps < hist[target]:
            hist[target] = steps

        diff = target - loc
        if steps + diff.imag + diff.real >= hist[target]:
            continue

        for dirn in [1, 1j, -1, -1j]:
            if loc + dirn in free and hist[loc + dirn] > steps + 1:
                queue.append((loc + dirn, steps + 1))
                hist[loc + dirn] = steps + 1

    return hist[target]


def run_algo_bfs(free, loc, target):

    queue = [(loc, 0)]
    hist = {loc}

    while len(queue) > 0:
        loc, steps = queue.pop(0)

        if loc == target:
            return steps

        for dirn in [1, 1j, -1, -1j]:
            if loc + dirn in free and loc + dirn not in hist:
                queue.append((loc + dirn, steps + 1))
                hist.add(loc+dirn)

    return math.inf



def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=18, year=2024).data

    S = 7 if example_run else 71
    loc, target = 0, (S-1) + (S-1)*1j
    lim = 12 if example_run else 1024
    free = [i + j*1j for (i, j) in product(range(S), repeat=2) if f"{i},{j}" not in data[0:lim]]

    result_part1 = run_algo_bfs(free, loc, target)

    for lim in count(len(data), -1):
        free = [i + j * 1j for (i, j) in product(range(S), repeat=2) if f"{i},{j}" not in data[0:lim]]
        res = run_algo_bfs(free, loc, target)
        if not math.isinf(res):
            break

    result_part2 = data[lim]

    extra_out = {'Number of bytes in input': len(data),
                 'Number of bytes that still (just) work': lim}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
