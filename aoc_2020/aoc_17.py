from typing import Union
from util.util import ProcessInput, run_day
import numpy as np
import itertools

debug = False


def count_neighbours_3d(grid, loc):
    return grid[max(loc[0] - 1, 0):min(loc[0] + 2, grid.shape[0]),
                max(loc[1] - 1, 0):min(loc[1] + 2, grid.shape[1]),
                max(loc[2] - 1, 0):min(loc[2] + 2, grid.shape[2])].sum()


def count_neighbours_4d(grid, loc):
    return grid[max(loc[0] - 1, 0):min(loc[0] + 2, grid.shape[0]),
                max(loc[1] - 1, 0):min(loc[1] + 2, grid.shape[1]),
                max(loc[2] - 1, 0):min(loc[2] + 2, grid.shape[2]),
                max(loc[3] - 1, 0):min(loc[3] + 2, grid.shape[3])].sum()


def run_all(example_run: Union[int, bool]):
    data = ProcessInput(example_run=example_run, day=17).data
    n_cycles = 6

    grid = np.array([[1 if x == '#' else 0 for x in row] for row in data])
    dims = (len(grid), len(grid[0]), 1)
    grid = grid.reshape(dims)
    for i in range(n_cycles):
        for ax in [0, 1, 2]:
            if np.sum(grid.take(0, axis=ax)) >= 3:
                grid = np.concatenate([np.zeros(dims[:ax] + (1,) + dims[ax + 1:]), grid], ax)
                dims = grid.shape
            if np.sum(grid.take(-1, axis=ax)) >= 3:
                grid = np.concatenate([grid, np.zeros(dims[:ax] + (1,) + dims[ax + 1:])], ax)
                dims = grid.shape

        old_grid = grid.copy()
        for x, y, z in itertools.product(range(dims[0]), range(dims[1]), range(dims[2])):
            if old_grid[x, y, z] == 1:
                grid[x, y, z] = 1 if count_neighbours_3d(old_grid, (x, y, z)) - 1 in (2, 3) else 0
            else:
                grid[x, y, z] = 1 if count_neighbours_3d(old_grid, (x, y, z)) == 3 else 0

        # Shrink grid if possible
        pad_length = 1  # How many rows / cols / layers need to be fully 0 to remove the outer row, columns, layer
        for ax in [0, 1, 2]:
            if np.sum(grid.take(range(pad_length), axis=ax)) == 0:
                grid = grid.take(range(1, dims[ax]), axis=ax)
                dims = grid.shape
            if np.sum(grid.take(range(-pad_length, 0), axis=ax)) == 0:
                grid = grid.take(range(0, dims[ax] - 1), axis=ax)
                dims = grid.shape

        if debug:
            print(f"{i}: {int(np.sum(grid))}, {old_grid.shape}, {grid.shape}"
                  f"{' --> Shrunk' if grid.shape != old_grid.shape else ''}")

    result_part1 = int(np.sum(grid))

    grid = np.array([[1 if x == '#' else 0 for x in row] for row in data])
    dims = (len(grid), len(grid[0]), 1, 1)
    grid = grid.reshape(dims)
    for i in range(n_cycles):
        for ax in [0, 1, 2, 3]:
            if np.sum(grid.take(0, axis=ax)) >= 3:
                grid = np.concatenate([np.zeros(dims[:ax] + (1,) + dims[ax + 1:]), grid], ax)
                dims = grid.shape
            if np.sum(grid.take(-1, axis=ax)) >= 3:
                grid = np.concatenate([grid, np.zeros(dims[:ax] + (1,) + dims[ax + 1:])], ax)
                dims = grid.shape

        old_grid = grid.copy()
        for x, y, z, w in itertools.product(range(dims[0]), range(dims[1]), range(dims[2]), range(dims[3])):
            if old_grid[x, y, z, w] == 1:
                grid[x, y, z, w] = 1 if count_neighbours_4d(old_grid, (x, y, z, w)) - 1 in (2, 3) else 0
            else:
                grid[x, y, z, w] = 1 if count_neighbours_4d(old_grid, (x, y, z, w)) == 3 else 0

        # Shrink grid if possible
        pad_length = 1  # How many rows / cols / layers need to be fully 0 to remove the outer row, columns, layer
        for ax in [0, 1, 2, 3]:
            if np.sum(grid.take(range(pad_length), axis=ax)) == 0:
                grid = grid.take(range(1, dims[ax]), axis=ax)
                dims = grid.shape
            if np.sum(grid.take(range(-pad_length, 0), axis=ax)) == 0:
                grid = grid.take(range(0, dims[ax] - 1), axis=ax)
                dims = grid.shape

        if debug:
            print(f"{i}: {int(np.sum(grid))}, {old_grid.shape}, {grid.shape}"
                  f"{' --> Shrunk' if grid.shape != old_grid.shape else ''}")

    result_part2 = int(np.sum(grid))

    extra_out = {'Dimension in input': len(data),
                 'Final dimension': grid.shape}  # TODO: create dict of additional things to have them printed

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
