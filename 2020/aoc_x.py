import numpy as np
import z3
import functools
import itertools
from typing import Union
from util import timing
import tqdm


debug = False

# Ideas:
# - Input process function that returns a list of ints by row
# - Input process function that returns a list of ints by block (until empty row)
# - Input process function that converts a block into a single row
# - Input process function that can return a list based on filtering out some pattern


@timing
def run_all(example_run: Union[int, bool]):

    file = f'aoc_x_exampledata{example_run}' if example_run else 'aoc_x_data'
    with open(file) as f:  # TODO: create utility function for this that can deal with various input types -> https://github.com/alexander-yu/adventofcode/blob/master/utils.py -> parse
        data = f.readlines()  # TODO: replace with pathlib.Path:  adj_data = pathlib.Path(file).read_text().rstrip('\n')
    adj_data = [row.rstrip('\n') for row in data]

    result_part1 = "TODO"
    result_part2 = "TODO"

    print(f'\nResults for {f"example" if example_run else "my"} input{f" {example_run}" if example_run else ""}:')
    print(f' Result of part 1: {result_part1}')
    print(f' Result of part 2: {result_part2}')

    print(f'\nDescriptives: \n TODO \n')


if __name__ == "__main__":
    [run_all(example_run=i) for i in [1]]
    run_all(example_run=False)
