from typing import Union
from util.util import ProcessInput, run_day

debug = False


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=24, year=2020).data

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
    #   - also, update to which set white points belong: having 1, 2, or more neighbours
    #       - all with 2 neighbours are added to the set for next day
    # - repeat 100 times
    points = set([point[0] + point[1] * 1j for point in points])
    neighbours = [(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)]
    neighbours = [point[0] + point[1] * 1j for point in neighbours]
    for day in range(100):
        new_points = set()
        white_sets = [set() for _ in range(2+1)]
        for point in points:
            this_count = 0
            for neighbour in neighbours:
                this_neighbour = point + neighbour
                if this_neighbour in points:
                    this_count += 1
                else:
                    not_present = True
                    for i in range(0, 2):
                        if not_present and this_neighbour in white_sets[i]:
                            not_present = False
                            white_sets[i].remove(this_neighbour)
                            white_sets[i+1].add(this_neighbour)
                    if not_present and this_neighbour not in white_sets[2]:
                        white_sets[0].add(this_neighbour)
            if this_count in (1, 2):
                new_points.add(point)
        points = new_points.union(white_sets[1])
        if debug:
            print(f"Day {day+1}: {len(points)}")

    result_part2 = len(points)

    extra_out = {'Number of rows in input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
