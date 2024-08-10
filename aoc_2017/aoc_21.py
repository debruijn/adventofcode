from itertools import product
from typing import Union
from util.util import ProcessInput, run_day

flips2 = [[0, 1, 2, 3], [2, 3, 0, 1], [1, 0, 3, 2], [3, 2, 1, 0],
          [2, 0, 3, 1], [1, 3, 0, 2], [0, 2, 1, 3], [3, 1, 2, 0]]
flips3 = [[0, 1, 2, 3, 4, 5, 6, 7, 8], [2, 1, 0, 5, 4, 3, 8, 7, 6], [6, 7, 8, 3, 4, 5, 0, 1, 2],
          [8, 7, 6, 5, 4, 3, 2, 1, 0], [6, 3, 0, 7, 4, 1, 8, 5, 2], [2, 5, 8, 1, 4, 7, 0, 3, 6],
          [0, 3, 6, 1, 4, 7, 2, 5, 8], [8, 5, 2, 7, 4, 1, 6, 3, 0]]


def get_flips(m_from):
    if len(m_from) % 2 == 0:
        return ["".join([m_from[x] for x in flip]) for flip in flips2]
    if len(m_from) % 3 == 0:
        return ["".join([m_from[x] for x in flip]) for flip in flips3]


def generate_art(grid, n_iter, mapping):
    size = len(grid)
    for i in range(n_iter):

        # Detect which rule to use: 2 or 3
        n_split = 2 if size % 2 == 0 else 3
        n_squares = int(size // n_split)

        # Split grid into subsquares
        split_squares = {}
        for k, l in product(range(n_squares), repeat=2):
            this_sq = [x[l*n_split:(l+1)*n_split] for x in grid[k*n_split:(k+1)*n_split]]
            split_squares[(k, l)] = "".join(this_sq)

        # Apply transformation to each subsquare
        for k, v in split_squares.items():
            split_squares[k] = mapping[v]

        # Merge back together as a bigger grid
        new_n = 4 if n_split == 3 else 3
        grid = [[] for _ in range(n_squares*new_n)]
        for k, l in product(range(n_squares), repeat=2):
            this_sq = split_squares[(k, l)]
            this_sq = [this_sq[j*new_n:(j+1)*new_n] for j in range(new_n)]
            [grid[k*new_n + j].append(this_sq[j]) for j in range(new_n)]
        grid = ["".join(x) for x in grid]
        size = len(grid)
    return grid


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=21, year=2017).data

    # Make a mapping from input, incl all rotations and flips
    mapping = {}
    for row in data:
        m_from, m_to = [x.replace('/', '') for x in row.split(' => ')]
        [mapping.update({x: m_to}) for x in get_flips(m_from)]

    # Apply art generation process
    grid = [".#.", "..#", "###"]
    n_iter = 2 if example_run else 5
    grid = generate_art(grid, n_iter, mapping)
    result_part1 = sum([sum([x == '#' for x in row]) for row in grid])

    # Do further iterations for part 2 (no need to restart)
    n_iter = 0 if example_run else 18 - n_iter
    grid = generate_art(grid, n_iter, mapping)
    result_part2 = sum([sum([x == '#' for x in row]) for row in grid])

    extra_out = {'Number of transformations in input': len(data),
                 'Final grid size': len(grid)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
