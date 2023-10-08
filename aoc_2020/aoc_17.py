from typing import Union
from util.util import ProcessInput, run_day
import numpy as np
import itertools

debug = False


def count_neighbours(grid, loc, n_dim):
    if n_dim == 3:
        return grid[max(loc[0] - 1, 0):min(loc[0] + 2, grid.shape[0]),
                    max(loc[1] - 1, 0):min(loc[1] + 2, grid.shape[1]),
                    max(loc[2] - 1, 0):min(loc[2] + 2, grid.shape[2])].sum()
    if n_dim == 4:
        return grid[max(loc[0] - 1, 0):min(loc[0] + 2, grid.shape[0]),
                    max(loc[1] - 1, 0):min(loc[1] + 2, grid.shape[1]),
                    max(loc[2] - 1, 0):min(loc[2] + 2, grid.shape[2]),
                    max(loc[3] - 1, 0):min(loc[3] + 2, grid.shape[3])].sum()


def conway_cubes(grid, n_dim, n_cycles):

    dims = (len(grid), len(grid[0])) + (1,) * (n_dim-2)
    grid = grid.reshape(dims)
    count_shrunk = 0

    for i in range(n_cycles):
        for ax in range(n_dim):
            if np.sum(grid.take(0, axis=ax)) >= 3:
                grid = np.concatenate([np.zeros(dims[:ax] + (1,) + dims[ax + 1:]), grid], ax)
                dims = grid.shape
            if np.sum(grid.take(-1, axis=ax)) >= 3:
                grid = np.concatenate([grid, np.zeros(dims[:ax] + (1,) + dims[ax + 1:])], ax)
                dims = grid.shape

        old_grid = grid.copy()
        for x_vec in list(itertools.product(*[range(dims[i]) for i in range(n_dim)])):
            if old_grid[x_vec] == 1:
                grid[x_vec] = 1 if count_neighbours(old_grid, x_vec, n_dim) - 1 in (2, 3) else 0
            else:
                grid[x_vec] = 1 if count_neighbours(old_grid, x_vec, n_dim) == 3 else 0

        # Shrink grid if possible
        pad_length = 1  # How many rows / cols / layers need to be fully 0 to remove the outer row, columns, layer
        for ax in range(n_dim):
            if np.sum(grid.take(range(pad_length), axis=ax)) == 0:
                grid = grid.take(range(1, dims[ax]), axis=ax)
                dims = grid.shape
            if np.sum(grid.take(range(-pad_length, 0), axis=ax)) == 0:
                grid = grid.take(range(0, dims[ax] - 1), axis=ax)
                dims = grid.shape

        count_shrunk = count_shrunk + 1 if grid.shape != old_grid.shape else count_shrunk
        if debug:
            print(f"{i}: {int(np.sum(grid))}, {old_grid.shape}, {grid.shape}"
                  f"{' --> Shrunk' if grid.shape != old_grid.shape else ''}")

    return int(np.sum(grid)), grid.shape, count_shrunk


def run_all(example_run: Union[int, bool]):
    data = ProcessInput(example_run=example_run, day=17).data
    n_cycles = 6

    grid = np.array([[1 if x == '#' else 0 for x in row] for row in data])

    result_3d = conway_cubes(grid, n_dim=3, n_cycles=n_cycles)
    result_part1 = result_3d[0]

    result_4d = conway_cubes(grid, n_dim=4, n_cycles=n_cycles)
    result_part2 = result_4d[0]

    extra_out = {'Size in input': len(data),
                 'Final size in 3d': result_3d[1],
                 'Nr of times shrunk in 3d': result_3d[2],
                 'Final size in 4d': result_4d[1],
                 'Nr of times shrunk in 4d': result_4d[2]}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
