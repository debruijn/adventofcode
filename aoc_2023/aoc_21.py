from typing import Union
from util.util import ProcessInput, run_day
import numpy as np

debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=21, year=2023).data

    # Part A: naive implementation, without being smart -> classic BFS
    N = 64 if not example_run else 6
    free = []
    start = 0
    for i, row in enumerate(data):
        for j, el in enumerate(row):
            if el == '.':
                free.append(i + j*1j)
            if el == 'S':
                start = i + j*1j
                free.append(i + j*1j)

    # Actual BFS algorithm starts here. Stopping criterion: we are over N!
    queue = [(start, 0)]
    end_at_N = set()

    while len(queue) > 0:
        curr_loc, curr_steps = queue.pop(0)
        if curr_steps<N:
            for i_dir in [1, -1, 1j, -1j]:
                this_loc = curr_loc + i_dir
                if this_loc in free and (this_loc, curr_steps + 1) not in queue:
                    queue.append((this_loc, curr_steps + 1))
                    if curr_steps+1 == N:
                        end_at_N.add(this_loc)

    result_part1 = len(end_at_N)

    # Part B: single-maps will converge to two parities after a while. You can directly reach the "other" S locs for
    # the actual input, so you will get there first every len(data) steps. In other words: you will start a new cycle
    # every len(data) steps. This will be started for more and more maps: 1 goes to 4, to 9, to 16, etc -> quadratic!
    # You can validate this by looking at the number of reachable locs every len(data) steps and take the double diff
    # (like in day 9) -> this will show a constant double-diff after a certain number of steps.
    # For the requested N, we need to know the "cycle" of it, so take modulo len(data), and then increase that by
    # 2*len(data) to have that cycle point three times (to fit the parabola). Run normal algorithm to that point, keeping
    # track of reachable number. Fit function, and apply to the requested N.

    # Note: the BFS here is improved vs the A version: it separately keeps track of odd and even visits, and doesn't keep
    # readding them.

    if not example_run:  # Does not work for example: no direct line between S and S.
        Actual_N = 26501365
        N = (Actual_N % len(data)) + 2 * len(data)
        queue = [(start, 0)]
        visited_odd = set()
        visited_even = set()
        rel_visited = []
        len_visited = [1,]
        ref_steps = 0

        while len(queue) > 0:
            curr_loc, curr_steps = queue.pop(0)
            if curr_steps > ref_steps:
                len_visited.append(len(rel_visited))
                ref_steps += 1
            if curr_steps <N:
                for i_dir in [1, -1, 1j, -1j]:
                    this_loc = curr_loc + i_dir
                    adj_loc = (this_loc.real % len(data)) + (this_loc.imag % len(data[0])) * 1j
                    rel_visited = visited_even if (curr_steps + 1) % 2 == 0 else visited_odd
                    if adj_loc in free and this_loc not in rel_visited:
                        queue.append((this_loc, curr_steps + 1))
                        rel_visited.add(this_loc)
        len_visited.append(len(rel_visited))

        # Get the relevant X and Y points (X = nr of steps, Y = nr of reachable locs), and fit parabola
        mod_x = [Actual_N % len(data) + i*len(data) for i in (0, 1, 2)]
        mod_y = [len_visited[Actual_N % len(data) + i*len(data)] for i in (0, 1, 2)]
        a, b, c = np.polyfit(mod_x, mod_y, 2)

        result_part2 = int(np.round(a * Actual_N**2 + b * Actual_N + c))
    else:
        result_part2 = "N/A"

    extra_out = {'Dimension of input': (len(data), len(data[0])),
                 'Location of S': start}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
