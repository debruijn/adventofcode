from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=1, year=2024).as_list_of_ints().data
    left, right = list(), list()
    for (i, j) in data:
        left.append(i)
        right.append(j)

    result_part1 = sum(abs(i - j) for (i, j) in zip(sorted(left), sorted(right)))
    result_part2 = sum([i * right.count(i) for i in left])

    extra_out = {'Number of rows in input': len(data)}  # TODO: create dict of additional things to have them printed

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
