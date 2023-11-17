from typing import Union
from aocd import get_data
from util.util import timing, rows_to_chunks, list_set, get_example_data
from functools import reduce


debug = False


@timing
def run_all(example_run: Union[int, bool]):

    if example_run:
        adj_data = get_example_data(2020, 6, example_run-1)
    else:
        data_raw = get_data(day=6, year=2020)
        adj_data = [x for x in data_raw.split('\n')]
    adj_data = rows_to_chunks(adj_data)

    result_part1 = sum(len(reduce(lambda x, y: x.union(y), list_set(z))) for z in adj_data)
    result_part2 = sum(len(reduce(lambda x, y: x.intersection(y), list_set(z))) for z in adj_data)

    print(f'\nResults for {f"example" if example_run else "my"} input{f" {example_run}" if example_run else ""}:')
    print(f' Result of part 1: {result_part1}')
    print(f' Result of part 2: {result_part2}')


if __name__ == "__main__":
    [run_all(example_run=i) for i in [1, 2]]
    run_all(example_run=False)
