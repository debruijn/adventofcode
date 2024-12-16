import math
from collections import defaultdict
from typing import Union
from util.util import ProcessInput, run_day


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

    # Initialize variables for algorithm: queue, hist, curr_steps, and list of result.
    queue = defaultdict(list)
    queue[0].append((start, dirn, []))  # loc, direction, path
    curr_steps = 0
    hist = defaultdict(lambda: math.inf)
    hist[(start, dirn)] = 0
    no_increase = False
    res = []
    while len(queue) > 0:
        # If there are no more options for the current number of steps, increase to next best (unless we were done)
        if len(queue[curr_steps]) == 0:
            del queue[curr_steps]
            if no_increase:
                break
            else:
                curr_steps = min(queue.keys())

        # Pop from current queue
        loc, dirn, path = queue[curr_steps].pop()

        if loc == target:  # If we are at target, we add this path to set of solutions and will no longer increase steps
            no_increase = True  # Don't immediately break -> find others for same curr_steps
            res.append(path)

        # Add to queue: step forwards (if there is no wall)
        if loc + dirn in free and hist[(loc + dirn, dirn)] >= curr_steps + 1:
            this_path = path + [1] if len(path) == 0 or path[-1].imag != 0 else path[:-1] + [path[-1] + 1]
            queue[curr_steps+1].append((loc+dirn, dirn, this_path))
            hist[(loc+dirn, dirn)] = curr_steps + 1

        # Add to queue: rotate in either direction
        for rot in [1j, -1j]:
            if hist[(loc, dirn * rot)] >= curr_steps + 1000:
                queue[curr_steps + 1000].append((loc, dirn * rot, path + [rot]))
                hist[(loc, dirn * rot)] = curr_steps + 1000

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

    result_part1 = curr_steps
    result_part2 = len(spots_to_sit)

    extra_out = {'Size of grid': (len(data), len(data[0])),
                 'Number of different best routes to take': len(res)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2])