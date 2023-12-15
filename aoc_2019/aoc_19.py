import itertools
from typing import Union
from util.util import ProcessInput, run_day
from aoc_2019.intcode_pc import IntCodePC


debug = False


def run_pc(i, j, data):
    pc = IntCodePC(data)
    pc.add_input([i, j])
    out = pc.run_until_end()
    return out[0][0]



def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=19, year=2019).as_list_of_ints(',').data[0]

    grid = [['']*50 for _ in range(50)]

    count_affected_points = 0
    for i, j in itertools.product(range(50), range(50)):
        if run_pc(i, j, data) == 1:
            count_affected_points += 1 if run_pc(i, j, data) else 0
            grid[i][j] = '#'
        else:
            grid[i][j] = '.'

    if debug:  # We can plot the grid if we want
        for row in grid:
            this_row = ""
            for val in row:
                this_row += val
            print(this_row)

    result_part1 = count_affected_points

    # Initialize search
    inds_at_50 = [i for i in range(len(grid[-1])) if grid[-1][i] == '#']
    min_i, max_i = min(inds_at_50), max(inds_at_50)
    res = {}
    row_nr = 50
    stop = False
    coords = (0,0)

    while not stop:  # Shift range if needed, and check if square fits
        min_i = min_i if run_pc(row_nr, min_i, data) == 1 else min_i + 1
        max_i = max_i if run_pc(row_nr, max_i+1, data) == 0 else max_i + 1
        res[row_nr] = (min_i, max_i)
        if len(res) > 100 and max_i - min_i > 100:
            if res[row_nr-99][1]-99 >= min_i:
                stop = True
                coords = (min_i, row_nr - 99)
        row_nr += 1

    result_part2 = coords[1] * 10000 + coords[0]  # Swapped x and y around, oops

    extra_out = {'Length of input program': len(data),
                 'Final coords': coords,
                 'Last row': row_nr,
                 'Range in last row': (min_i, max_i)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [])
