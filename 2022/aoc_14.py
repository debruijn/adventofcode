import numpy as np
from typing import Union
from util import timing

debug = False


def do_part(adj_data: list, source: list, part_2: bool = False):

    # Find dimensions of grid
    borders = [source[0], source[0], source[1], source[1]]  # Max X, Min X, Max Y, Min Y
    for row in adj_data:
        borders[0] = max(borders[0], max([x[0] for x in row]))
        borders[1] = min(borders[1], min([x[0] for x in row]))
        borders[2] = max(borders[2], max([x[1] for x in row]))
        borders[3] = min(borders[3], min([x[1] for x in row]))
    if part_2:
        borders[2] += 2
        borders[1] = source[0] - borders[2] - 1
        borders[0] = source[0] + borders[2] + 1

    # Create starting grid
    grid = np.zeros([borders[0] - borders[1] + 1, borders[2] - borders[3] + 1])
    if part_2:
        grid[:, -1] = 1
    cornerpoint = np.array([borders[1], borders[3]])

    # Fill grid with rock paths
    for row in adj_data:
        prev_point = row[0]
        for point in row[1:]:
            if prev_point[0] == point[0]:
                for y in range(min(point[1], prev_point[1]), max(point[1], prev_point[1])+1):
                    grid[tuple((point[0], y) - cornerpoint)] = 1
            else:
                for x in range(min(point[0], prev_point[0]), max(point[0], prev_point[0])+1):
                    grid[tuple((x, point[1]) - cornerpoint)] = 1
            prev_point = point

    # Let sand fall
    stop = False
    n_sand = 0
    while not stop:
        loc_sand = source - cornerpoint

        # Stop if source is filled
        if grid[tuple(loc_sand)] == 1:
            stop = True
            can_move = False
        else:
            can_move = True

        while can_move:
            if loc_sand[1] + 1 >= grid.shape[1]:
                stop = True  # Stop if sand falls out of the bottom
                can_move = False
            elif grid[tuple(loc_sand + (0, 1))] == 0:
                loc_sand += (0, 1)
            elif loc_sand[0] - 1 < 0:
                stop = True  # Stop if sand falls out of the bottom
                can_move = False
            elif grid[tuple(loc_sand + (-1, 1))] == 0:
                loc_sand += (-1, 1)
            elif loc_sand[0] + 1 > grid.shape[0]:
                stop = True  # Stop if sand falls out of the bottom
                can_move = False
            elif grid[tuple(loc_sand + (1, 1))] == 0:
                loc_sand += (1, 1)
            else:
                can_move = False
        if not stop:
            n_sand += 1
            grid[tuple(loc_sand)] = 1

    return n_sand, borders


@timing
def run_all(example_run: Union[int, bool]):

    file = f'aoc_14_exampledata{example_run}' if example_run else 'aoc_14_data'
    with open(file) as f:
        data = f.readlines()
    adj_data = [row.rstrip('\n') for row in data]
    adj_data = [[np.array([int(z) for z in x.split(',')]) for x in row.split(' -> ')] for row in adj_data]
    source = [500, 0]

    result_part1 = do_part(adj_data, source)

    print(f'Results for {f"example" if example_run else "my"} input{f" {example_run}" if example_run else ""}:')
    print(f' Result of part 1: {result_part1[0]}')
    result_part2 = do_part(adj_data, source, part_2=True)
    print(f' Result of part 2: {result_part2[0]}')

    borders = result_part2[1]
    shape = (borders[0] - borders[1] + 1, borders[2] - borders[3] + 1)
    print(f'\nDescriptives: \n x range: {borders[1]} to {borders[0]} '
          f'\n y range: {borders[3]} to {borders[2]} '
          f'\n (size: {shape[0]} by {shape[1]}, {shape[0]*shape[1]} total elements) \n')


[run_all(example_run=i) for i in [1]]
run_all(example_run=False)
