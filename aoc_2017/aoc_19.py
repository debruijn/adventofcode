from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):
    data = ProcessInput(example_run=example_run, day=19, year=2017).data
    start = data[0].index('|')

    # Easier for indexing if grid is constructed with complex number indexing
    grid = {}
    for i, row in enumerate(data):
        for j, col in enumerate(row):
            if col == ' ':
                continue
            grid[i + j * 1j] = col

    # Initialize algorithm: start location and direction, and the required answers for part 1 and 2
    curr_loc = start * 1j
    curr_dir = 1
    recovered_letters = ""
    n_step = 0
    while True:
        n_step += 1
        if curr_loc + curr_dir not in grid:
            curr_dir = curr_dir * 1j if curr_loc + curr_dir * 1j in grid else curr_dir * -1j
            if curr_loc + curr_dir not in grid:
                break
        curr_loc += curr_dir
        if grid[curr_loc] not in "-|+":
            recovered_letters += grid[curr_loc]

    result_part1 = recovered_letters
    result_part2 = n_step

    extra_out = {'Dimensions of grid': f"{int(max(x.real for x in grid.keys())) + 1} x "
                                       f"{int(max(x.imag for x in grid.keys())) + 1}",
                 'Number of non-blank spaces': len(grid.keys()),
                 'Number of turning points': sum(x == '+' for x in grid.values())}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
