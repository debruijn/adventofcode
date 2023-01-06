from typing import Union
from util import timing, rows_to_chunks, list_set
from functools import reduce


debug = False


@timing
def run_all(example_run: Union[int, bool]):

    file = f'aoc_6_exampledata{example_run}' if example_run else 'aoc_6_data'
    with open(file) as f:
        data = f.readlines()
    adj_data = [row.rstrip('\n') for row in data]
    adj_data = rows_to_chunks(adj_data)

    result_part1 = sum(len(reduce(lambda x, y: x.union(y), list_set(z))) for z in adj_data)
    result_part2 = sum(len(reduce(lambda x, y: x.intersection(y), list_set(z))) for z in adj_data)

    print(f'\nResults for {f"example" if example_run else "my"} input{f" {example_run}" if example_run else ""}:')
    print(f' Result of part 1: {result_part1}')
    print(f' Result of part 2: {result_part2}')


if __name__ == "__main__":
    [run_all(example_run=i) for i in [1]]
    run_all(example_run=False)
