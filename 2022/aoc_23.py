import numpy as np
import pandas as pd
from typing import Union
from util.util import timing


debug = False


# Slow but no motivation to improve speed.
# Potential speed improvements:
# - avoid the many conversions of tuple -> array -> tuple (to make np indexing easier)
# - don't reconstruct map each time but continue with elves themselves (but might make it slower as well..)
# - work with imaginary numbers to speed up calcs


@timing
def run_all(example_run: Union[int, bool]):

    file = f'aoc_23_exampledata{example_run}' if example_run else 'aoc_23_data'
    with open(file) as f:
        data = f.readlines()
    adj_data = [row.rstrip('\n') for row in data]

    # Create initial map with some extra buffer around the elves
    map_dims = (len(data)+2, len(adj_data[0])+2)
    map = np.zeros(map_dims, dtype=int)
    for i in range(len(adj_data)):
        for j in range(len(adj_data[i])):
            map[i+1, j+1] = 1 if adj_data[i][j] == "#" else 0

    dir_proposal_order = [1, 0, 3, 2]  # N, S, W, E
    dir_proposal_order.reverse()  # I start at the back such that the final proposal will be the "first to be accepted"
    dir_checking = np.array((((1, -1), (1, 0), (1, 1)),     # S
                            ((-1, -1), (-1, 0), (-1, 1)),   # N
                            ((-1, 1), (0, 1), (1, 1)),      # E
                            ((-1, -1), (0, -1), (1, -1))))  # W

    map_prev = np.zeros_like(map)
    offset = (0, 0)

    r = 0
    moving_elves = []

    while not(map.shape == map_prev.shape and (map == map_prev).all()):
        r += 1
        elves = np.argwhere(map)
        proposal = {}
        for elf in elves:
            prop_elf = elf
            if map[elf[0]-1:elf[0]+2, elf[1]-1:elf[1]+2].sum() > 1:
                for dir in dir_proposal_order:
                    check_locs = tuple(tuple(x) for x in elf + dir_checking[dir])
                    if not any(map[loc] for loc in check_locs):
                        prop_elf = check_locs[1]
            proposal.update({tuple(elf): tuple(prop_elf)})

        unique_proposal = [x for x in proposal.values() if sum([x == y for y in proposal.values()]) == 1]
        new_elves = {x: proposal[x] if proposal[x] in unique_proposal else x for x in proposal}

        # Stop in case all elves stay at the same loc
        if all(elf == new_elves[elf] for elf in new_elves):
            if r <= 10:
                result_part1 = ((elves.max(axis=0) - elves.min(axis=0)) + np.array((1, 1))).prod() - elves.shape[0]
            break
        else:
            moving_elves.append(sum(elf != new_elves[elf] for elf in new_elves))
            if debug or True:
                print(f"{r}: {moving_elves[r-1]} moving elves.")

        # Check if some of the elves are close to the borders; if so update map dimension and offset
        if any(val[0] == map_dims[0]-1 for val in new_elves.values()):
            map_dims = (map_dims[0]+1, map_dims[1])
        if any(val[1] == map_dims[1]-1 for val in new_elves.values()):
            map_dims = (map_dims[0], map_dims[1]+1)
        if any(val[0] == 0 for val in new_elves.values()):
            offset = (offset[0]+1, offset[1])
            map_dims = (map_dims[0]+1, map_dims[1])
        if any(val[1] == 0 for val in new_elves.values()):
            offset = (offset[0], offset[1]+1)
            map_dims = (map_dims[0], map_dims[1]+1)

        # Create new (potentially bigger) map and put all elves on it
        map_prev = map.copy()
        map = np.zeros(map_dims)
        for elf in new_elves:
            elf_loc = new_elves[elf]
            elf_loc = (elf_loc[0] + offset[0], elf_loc[1] + offset[1])
            map[elf_loc] = 1

        # Reset offset and update direction
        offset = (0, 0)
        pop_dir = dir_proposal_order.pop()
        dir_proposal_order.insert(0, pop_dir)

        if debug:
            print(dir_proposal_order)
            print(map)

        if r == 10:
            elves = np.argwhere(map)
            result_part1 = ((elves.max(axis=0) - elves.min(axis=0)) + np.array((1, 1))).prod() - elves.shape[0]

    elves = np.argwhere(map)
    result_part2 = r

    print(f'\nResults for {f"example" if example_run else "my"} input{f" {example_run}" if example_run else ""}:')
    print(f' Result of part 1: {result_part1}')
    print(f' Result of part 2: {result_part2}')

    print(f'\nDescriptives: \n Number elves: {elves.shape[0]} \n'
          f' Initial map size: {(len(data)+2, len(adj_data[0])+2)}\n'
          f' Final map size: {map.shape}\n'
          f' Max number of moving elves: {max(moving_elves)}\n')

    pd.DataFrame(data={'moving_elves': moving_elves}).to_csv('aoc_23_movingelves.csv')


if __name__ == "__main__":
    [run_all(example_run=i) for i in [2, 1]]
    run_all(example_run=False)
