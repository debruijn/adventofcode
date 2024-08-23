from itertools import product
from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=8, year=2016).data
    debug = False

    grid_size = (6 if not example_run else 3, 50 if not example_run else 7)
    grid = [[0] * (grid_size[1]) for _ in range(grid_size[0])]

    for row in data:
        if row.startswith('rect'):
            dims = [int(x) for x in row.split()[1].split('x')]
            for i, j in product(range(dims[0]), range(dims[1])):
                grid[j][i] = 1
        if row.split()[1]=='column':
            col = int(row.split()[2].split('=')[1])
            shift = int(row.split()[-1])
            cl = [grid[i][col] for i in range(grid_size[0])]
            for i in range(grid_size[0]):
                grid[i][col] = cl[i - shift if 0 <= i - shift < grid_size[0] else - (shift-i)]
        if row.split()[1]=='row':
            rw = int(row.split()[2].split('=')[1])
            shift = int(row.split()[-1])
            grid[rw] = grid[rw][-shift:] + grid[rw][:-shift]

    result_part1 = sum(sum(x) for x in grid)

    if debug:
        [print("".join("#" if x == 1 else " " for x in row)) for row in grid]

    result_part2 = "ZJHRKCPLYJ" if not example_run else 'O\'\''  # Read from printed text if debug==True

    extra_out = {'Number of steps in input': len(data),
                 'Length of code': len(result_part2)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
