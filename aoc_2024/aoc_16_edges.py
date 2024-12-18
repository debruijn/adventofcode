import math
from collections import defaultdict
from typing import Union
from util.util import ProcessInput, run_day, grid_to_corners
import heapq
from itertools import count, pairwise


# Test use of `grid_to_corners` from my util package that converts a grid to only the key points as a graph
# Warning: I am not solving the actual AoC 2024 day 16 here because I ignore the rotation cost.

def run_all(example_run: Union[int, bool]):

    # Process input to list of available locations, start location, target location and start direction
    data = ProcessInput(example_run=example_run, day=16, year=2024).data
    rot_cost = 0
    edges = grid_to_corners(data, free = '.SE', mark='SE', rot_cost=rot_cost)
    start, target, dirn = 0, 0, 1j
    for i, row in enumerate(data):
        for j, el in enumerate(row):
            if el == 'S':
                start = (i, j)
            if el == 'E':
                target = (i, j)

    # Initialize variables for algorithm: heap as priority queue, hist, best result, and list of result.
    heap = [(0, 0, start, dirn, [(start, 0)])]
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

        # Add to queue: neighbors in graph
        for nxt, step in edges[loc].items():
            if hist[(nxt, dirn)] >= curr_steps + step:
                this_path = path + [(nxt, step)]
                heapq.heappush(heap, (curr_steps+step, next(counter), nxt, dirn, this_path))
                hist[(nxt, dirn)] = curr_steps + step

    # Process resulting paths by checking unique paths connecting points (count intermediate steps) and all connections
    unique_paths = set([(x[0][0], x[1][0], x[1][1]) for rs in res for x in pairwise(rs)])
    len_unique_paths = sum([x[2] - 1 for x in unique_paths])
    nr_connecting_points = len(set([x[0] for rs in res for x in rs]))

    result_part1 = best
    result_part2 = len_unique_paths + nr_connecting_points

    extra_out = {'Size of grid': (len(data), len(data[0])),
                 'Number of different best routes to take': len(res),
                 'Length of first best route': len(res[0]) if len(res)>0 else ""}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2])
