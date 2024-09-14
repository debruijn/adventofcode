from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=25, year=2015).data[0]

    def get_index(row, col):
        prev_top_row = row + col - 2
        index_prev_top_row = sum(i for i in range(1, prev_top_row+1))  # Top row index follows cumulative sum
        return index_prev_top_row + col  # Actual index is it's last previous top row index + column number

    # Inputs from text
    curr_val = 27995004
    mult = 252533
    div = 33554393
    curr = (6, 6)
    target = (int(data.split()[-3][:-1]), int(data.split()[-1][:-1]))  # Personal input

    # Get "flattened" indices for curr and target
    curr_ind = get_index(*curr)
    target_ind = get_index(*target)

    # Loop from curr to target and update curr_val that many times.
    for _ in range(curr_ind, target_ind):
        curr_val = (curr_val * mult) % div

    result_part1 = curr_val
    result_part2 = "Merry Christmas!"

    extra_out = {'Target location': target,
                 'Start index': get_index(*curr),
                 'Target index': target_ind}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [])
