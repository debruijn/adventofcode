import math
from collections import defaultdict
from typing import Union
from util.util import ProcessInput, run_day
import heapq
from itertools import count


# Ideas for speedup (since 6.2s with Pypy is a bit too slow for me):
# v Try if heapq is faster than my defaultdict implementation -> tested, not really the cases, but will use itt for now
# - Preprocess grid to corners, and create cost to go from corner to corner (with or without rotating)
# - Reimplement in Rust ->
#       only need to pass free, start and target along so little overhead to Rust
#       only need to return res and curr_steps so little overhead back as well (or can also process res in Rust)
# - Try out networkx (although I want to be pure Python (except for Rust) as much as possible)


def run_all(example_run: Union[int, bool]):

    # Process input to list of available locations, start location, target location and start direction
    data = ProcessInput(example_run=example_run, day=16, year=2024).data
    free, start, target, dirn = [], 0, 0, 1j
    for i, row in enumerate(data):
        for j, el in enumerate(row):
            if el == '.' or el == 'S' or el == 'E':
                free.append(i +j*1j)
                if el == 'S':
                    start = i + j*1j
                if el == 'E':
                    target = i + j*1j

    # Initialize variables for algorithm: heap as priority queue, hist, best result, and list of result.
    heap = [(0, 0, start, dirn, [])]
    heapq.heapify(heap)
    counter = count()  # Utility counter as 2nd priority to avoid comparing the locations in case of tied 1st priority
    hist = defaultdict(lambda: math.inf)
    hist[(start, dirn)] = 0
    res = []
    best = math.inf
    while len(heap) > 0:
        # Pop from heap and stop if worse than found solution
        curr_steps, _, loc, dirn, path = heapq.heappop(heap)
        if curr_steps > best:
            break

        if loc == target:  # If we are at target, we add this path to set of solutions and will no longer increase steps
            best = curr_steps
            res.append(path)

        # Add to queue: step forwards (if there is no wall)
        if loc + dirn in free and hist[(loc + dirn, dirn)] >= curr_steps + 1:
            this_path = path + [1] if len(path) == 0 or path[-1].imag != 0 else path[:-1] + [path[-1] + 1]
            heapq.heappush(heap, (curr_steps+1, next(counter), loc+dirn, dirn, this_path))
            hist[(loc+dirn, dirn)] = curr_steps + 1

        # Add to queue: rotate in either direction
        # -> Slight speedup: immediately take two steps (if both steps are in 'free') and if not possible, don't turn
        for rot in [1j, -1j]:
            r_dirn = dirn * rot
            if loc + r_dirn in free and loc + 2 * r_dirn in free and hist[(loc + 2 * r_dirn, r_dirn)] >= curr_steps + 1002:
                heapq.heappush(heap, (curr_steps + 1002, next(counter), loc + 2 * r_dirn, r_dirn, path + [rot, 2]))
                hist[(loc + 2 * r_dirn, r_dirn)] = curr_steps + 1002

    # Process resulting paths (that were compressed for memory reasons) -> which points are visited?
    spots_to_sit = {start}
    for path in res:
        loc = start
        dir = 1j
        for step in path:
            if step.imag != 0:
                dir *= step
                continue
            for _ in range(step):
                loc += dir
                spots_to_sit.add(loc)

    result_part1 = best
    result_part2 = len(spots_to_sit)

    extra_out = {'Size of grid': (len(data), len(data[0])),
                 'Number of different best routes to take': len(res),
                 'Length of first best route': len(res[0])}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2])
