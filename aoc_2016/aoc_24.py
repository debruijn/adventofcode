from collections import defaultdict
from itertools import combinations, permutations
from typing import Union
from util.util import ProcessInput, run_day


def process_grid(data):
    # Process grid into where nums and free spaces are, using complex notation
    free = []
    nums = {}
    for i, row in enumerate(data):
        for j, col in enumerate(row):
            if col != '#':
                free.append(i + j*1j)
                if col != '.':
                    nums[int(col)] = i + j*1j
    return free, nums


def get_distances(free, nums):
    # Get minimal distance between each pair of points, using a simple BFS for each combination of points
    dist = defaultdict(dict)
    for x, y in combinations(nums.keys(), 2):
        this_loc = nums[x]
        this_dist = 0
        queue = [(this_loc, this_dist)]
        hist = []
        while len(queue) > 0:
            this_loc, this_dist = queue.pop(0)
            if this_loc == nums[y]:
                break
            for step in (1, -1, 1j, -1j):
                new_loc = this_loc + step
                if new_loc in free and new_loc not in hist:
                    hist.append(new_loc)
                    queue.append((new_loc, this_dist + 1))
        dist[x][y] = this_dist
        dist[y][x] = this_dist

    return dist


def get_greedy_upperbound(dist, nums, back_to_zero=False):
    # Greedy approach (go to nearest point each time; without considering later steps) -> upperbound for later steps.
    todo = list(nums.keys())
    curr = 0
    todo.remove(curr)
    total_dist = 0
    while len(todo) > 0:
        this = min([x for x in dist[curr] if x in todo], key=lambda x: dist[curr][x])
        total_dist += dist[curr][this]
        curr = this
        todo.remove(curr)
    if back_to_zero:  # Part 2
        total_dist += dist[curr][0]

    return total_dist


def get_min_total_distance(dist, nums, back_to_zero=False):
    # Upperbound - not really needed since I can loop over all options anyway but could be useful in another approach.
    min_dist = get_greedy_upperbound(dist, nums, back_to_zero)
    for order in permutations([x for x in range(1, (len(nums)))]):
        this_dist = 0
        curr = 0
        for i in order:
            this_dist += dist[curr][i]
            curr = i
        if back_to_zero:
            this_dist += dist[curr][0]  # Part 2
        if this_dist < min_dist:
            min_dist = this_dist

    return min_dist


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=24, year=2016).data

    free, nums = process_grid(data)
    dist = get_distances(free, nums)

    result_part1 = get_min_total_distance(dist, nums)
    result_part2 = get_min_total_distance(dist, nums, back_to_zero=True)

    extra_out = {'Number of nums in grid': len(nums),
                 'Size of grid': (len(data), len(data[0]))}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
