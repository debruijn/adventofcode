from typing import Union
from util.util import ProcessInput, run_day
from collections import Counter

debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=24).data

    # Part 1:
    # - count steps in all directions
    # - convert three directions into their opposite direction (ne => -sw)
    # - convert "e" direction into "se" and "-sw" -> 2D coordinate
    # - see if 2D coordinate in set of points; if so, add it; if not, remove it
    # - count nr of points
    this_dir = ['se', 'sw', 'ne', 'nw', 'e', 'w']
    opp_dir = ['nw', 'ne', 'sw', 'se', 'w', 'e']
    points = []
    for row in data:
        net_direction = {}
        for dir_i in this_dir:
            if dir_i in ['ne', 'nw', 'w']:
                this_opp_dir = opp_dir[this_dir.index(dir_i)]
                net_direction[this_opp_dir] = net_direction[this_opp_dir] - row.count(dir_i)
            else:
                net_direction[dir_i] = row.count(dir_i)
            row = row.replace(dir_i, '')  # Remove direction to avoid counting "se" as "e"

        this_point = (net_direction['se'] + net_direction['e'], net_direction['sw'] - net_direction['e'])
        points.remove(this_point) if this_point in points else points.append(this_point)

    result_part1 = len(points)

    # Part 2:
    # - convert (2d) points to imaginary numbers for ease of manipulation
    # - define neighbours: |diff|<=1 per axis, and they are not both 1 or both -1
    # - for each point that is points, determine whether neighbours are points
    #   - if 1 or 2 of them are, keep this point for the next day
    #   - also, keep a running total for how many times neighbours not in points are checked
    #       - if that count is 2, add to the set for next day
    # - repeat 100 times
    points = [point[0] + point[1] * 1j for point in points]
    neighbours = [(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)]
    neighbours = [point[0] + point[1] * 1j for point in neighbours]
    for day in range(100):
        new_points = []
        white_with_neighbours = Counter()
        for point in points:
            this_neighbours = [point + neighbour for neighbour in neighbours]
            this_count = 0
            for neighbour in this_neighbours:
                if neighbour in points:
                    this_count += 1
                else:
                    white_with_neighbours[neighbour] += 1
            if this_count in (1, 2):
                new_points.append(point)
        for white, count in white_with_neighbours.items():
            if count == 2:
                new_points.append(white)
        if debug:
            print(f"Day {day+1}: {len(new_points)}")
        points = new_points

    result_part2 = len(points)

    extra_out = {'Number of rows in input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
