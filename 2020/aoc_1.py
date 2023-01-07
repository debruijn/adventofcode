from typing import Union
from util.util import timing
import itertools


debug = False


@timing
def run_all(example_run: Union[int, bool]):

    file = f'aoc_1_exampledata{example_run}' if example_run else 'aoc_1_data'
    with open(file) as f:
        data = f.readlines()
    adj_data = [int(row.rstrip('\n')) for row in data]

    result_part1 = "TODO"
    result_part2 = "TODO"

    for x, y in itertools.combinations(adj_data, 2):
        if x + y == 2020:
            result_part1 = x * y

    for x, y, z in itertools.combinations(adj_data, 3):
        if x + y + z == 2020:
            result_part2 = x * y * z

    print(f'\nResults for {f"example" if example_run else "my"} input{f" {example_run}" if example_run else ""}:')
    print(f' Result of part 1: {result_part1}')
    print(f' Result of part 2: {result_part2}')


if __name__ == "__main__":
    [run_all(example_run=i) for i in [1]]
    run_all(example_run=False)
