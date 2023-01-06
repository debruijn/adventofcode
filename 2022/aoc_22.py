import numpy as np
from typing import Union
from util import timing
import tqdm
import re


debug = False

side_mapping_example = {
    1: {'L': (3, 'D', 0), 'U': (2, 'D', 1), 'R': (6, 'L', 1)},
    2: {'U': (1, 'D', 1), 'D': (5, 'U', 1), 'L': (6, 'U', 1)},
    3: {'U': (1, 'R', 0), 'D': (5, 'R', 1)},
    4: {'R': (6, 'D', 1)},
    5: {'L': (3, 'U', 1), 'D': (2, 'U', 1)},
    6: {'U': (4, 'L', 1), 'R': (1, 'L', 1), 'D': (2, 'R', 1)}
                        }

side_mapping_data = {
    1: {'L': (4, 'R', 1), 'U': (6, 'R', 0)},
    2: {'U': (6, 'U', 0), 'R': (5, 'L', 1), 'D': (3, 'L', 0)},
    3: {'L': (4, 'D', 0), 'R': (2, 'U', 0)},
    4: {'L': (1, 'R', 1), 'U': (3, 'R', 0)},
    5: {'R': (2, 'L', 1), 'D': (6, 'L', 0)},
    6: {'L': (1, 'D', 0), 'R': (5, 'U', 0), 'D': (2, 'D', 0)}
                        }

map_dir = {'R': 0, 'D': 1, 'L': 2, 'U': 3}
inv_map_dir = {0: 'R', 1: 'D', 2: 'L', 3: 'U'}


def part1(data):

    adj_data = [[x for x in row.rstrip('\n')] for row in data]
    instructions = data[-1]
    max_len = max([len(row) for row in adj_data])
    map = np.ones((len(adj_data)-2, max_len), dtype=int) * -1

    for i in range(len(adj_data[:-2])):
        for j in range(len(adj_data[i])):
            map[i, j] = 1 if adj_data[i][j] == "#" else 0 if adj_data[i][j] == "." else -1

    steps = re.split("[RL]", instructions)  # Pycharm autocorrect from R|L
    turns = [x for x in instructions if x in ['R', 'L']]

    directions = (np.array((0, 1)), np.array((1, 0)), np.array((0, -1)), np.array((-1, 0)))
    dir_ind = 0  # To the right
    curr_loc = np.array((0, np.where(map[0, :] == 0)[0][0]))

    first_in_row = [np.where(row >= 0)[0][0] for row in map]
    first_in_col = [-1 if len(np.where(row >= 0)[0]) == 0 else np.where(row >= 0)[0][0] for row in map.transpose()]
    last_in_row = [np.where(row >= 0)[0][-1] for row in map]
    last_in_col = [-1 if len(np.where(row >= 0)[0]) == 0 else np.where(row >= 0)[0][-1] for row in map.transpose()]

    for i in tqdm.trange(len(steps)):

        # Do step i
        for j in range(int(steps[i])):
            cand_loc = curr_loc + directions[dir_ind]
            if any(cand_loc >= np.array(map.shape)) or any(cand_loc < 0) or map[tuple(cand_loc)] == -1:  # We go off the map
                if dir_ind == 0:  # Right
                    cand_loc = np.array([curr_loc[0], first_in_row[curr_loc[0]]])
                elif dir_ind == 2:  # Left
                    cand_loc = np.array([curr_loc[0], last_in_row[curr_loc[0]]])
                elif dir_ind == 1:  # Down
                    cand_loc = np.array([first_in_col[curr_loc[1]], curr_loc[1]])
                else:  # Up
                    cand_loc = np.array([last_in_col[curr_loc[1]], curr_loc[1]])
            if map[tuple(cand_loc)] == 0:
                curr_loc = cand_loc

        # Do turn i (if i < len(turns))
        if i < len(turns):
            dir_ind = (dir_ind + 1) % 4 if turns[i] == 'R' else (dir_ind - 1) % 4

        if debug:
            print(f"{i}: {curr_loc}, {steps[i]}, {directions[dir_ind]}, {cand_loc}")

    return (curr_loc[0]+1) * 1000 + (curr_loc[1]+1)*4 + dir_ind


def part2(data, side_mapping):

    instructions = data[-1]
    adj_data = [[x for x in row.rstrip('\n')] for row in data]
    max_len = max([len(row.rstrip('\n')) for row in data])
    map = np.ones((len(data)-2, max_len), dtype=int) * -1

    for i in range(len(adj_data[:-2])):
        for j in range(len(adj_data[i])):
            map[i, j] = 1 if adj_data[i][j] == "#" else 0 if adj_data[i][j] == "." else -1

    steps = re.split("[RL]", instructions)  # Pycharm autocorrect from R|L
    turns = [x for x in instructions if x in ['R', 'L']]

    directions = (np.array((0, 1)), np.array((1, 0)), np.array((0, -1)), np.array((-1, 0)))
    dir_ind = 0  # To the right
    curr_loc = np.array((0, np.where(map[0, :] == 0)[0][0]))

    # Process map to the 6 sides, with the coordinates
    # Figure out how to map each side to another side when you go off of it
    # So like: "If you leave side 4 to the right, you end up at side 6 going down"
    n_s = int(((map.shape[0] * map.shape[1] - (map == -1).sum()) / 6)**0.5)
    sides = np.ones_like(map) * -1
    find_sides = map[(range(0, map.shape[0], n_s))][:, range(0, map.shape[1], n_s)]
    curr_side = 1
    for i in range(find_sides.shape[0]):
        for j in range(find_sides.shape[1]):
            if find_sides[i, j] > -1:
                sides[n_s*i:n_s*(i+1), n_s*j:n_s*(j+1)] = curr_side
                curr_side += 1

    for i in tqdm.trange(len(steps)):

        # Do step i
        for j in range(int(steps[i])):
            cand_loc = curr_loc + directions[dir_ind]
            new_dir = dir_ind
            if any(cand_loc >= np.array(map.shape)) or any(cand_loc < 0) or map[tuple(cand_loc)] == -1:  # We go off the map

                side = side_mapping[sides[tuple(curr_loc)]]
                new_side = side[inv_map_dir[dir_ind]]
                new_dir = map_dir[new_side[1]]

                # Find loc of curr_loc in side
                curr_loc_side = curr_loc % n_s

                if dir_ind in [0, 2]:
                    keep_loc = curr_loc_side[0]
                else:
                    keep_loc = curr_loc_side[1]
                if new_side[2] == 1:
                    keep_loc = n_s - keep_loc - 1

                if new_dir == 1:
                    new_loc_side = [0, keep_loc]
                elif new_dir == 3:
                    new_loc_side = [n_s - 1, keep_loc]
                elif new_dir == 0:
                    new_loc_side = [keep_loc, 0]
                else:
                    new_loc_side = [keep_loc, n_s - 1]

                cand_loc = np.array(new_loc_side) + np.argwhere(sides == new_side[0])[0]

            if debug:
                print(f"{i, j}: {curr_loc}, {dir_ind}, {cand_loc}")

            if map[tuple(cand_loc)] == 0:
                curr_loc = cand_loc
                dir_ind = new_dir

        if debug:
            print(f"{i}: {curr_loc}, {steps[i]}, {directions[dir_ind]}, {cand_loc}")

        # Do turn i (if i < len(turns))
        if i < len(turns):
            dir_ind = (dir_ind + 1) % 4 if turns[i] == 'R' else (dir_ind - 1) % 4

    result = (curr_loc[0]+1) * 1000 + (curr_loc[1]+1)*4 + dir_ind

    stats = (len(steps), n_s)

    return result, stats


@timing
def run_all(example_run: Union[int, bool]):

    file = f'aoc_22_exampledata{example_run}' if example_run else 'aoc_22_data'
    with open(file) as f:
        data = f.readlines()
    adj_data = [[x for x in row.rstrip('\n')] for row in data]

    result_part1 = part1(data)
    result_part2, stats = part2(data, side_mapping_data if not example_run else side_mapping_example)

    print(f'\nResults for {f"example" if example_run else "my"} input{f" {example_run}" if example_run else ""}:')
    print(f' Result of part 1: {result_part1}')
    print(f' Result of part 2: {result_part2}')

    print(f'\nDescriptives: \n Number of steps and turns: {stats[0]} \n Size of side of cube: {stats[1]} \n')


if __name__ == "__main__":
    [run_all(example_run=i) for i in [1]]
    run_all(example_run=False)
