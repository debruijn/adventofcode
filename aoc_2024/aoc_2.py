from itertools import pairwise
from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=2, year=2024).as_list_of_ints().data

    count_safe = 0
    for row in data:
        if any(abs(i - j) > 3 for (i, j) in pairwise(row)):
            continue
        if all((i-j) > 0 for (i, j) in pairwise(row)) or all( (i-j) < 0 for (i, j) in pairwise(row)):
            count_safe += 1

    result_part1 = count_safe

    count_safe = 0
    for row in data:
        if all(abs(i - j) <= 3 for (i, j) in pairwise(row)) and (all((i-j) > 0 for (i, j) in pairwise(row)) or all( (i-j) < 0 for (i, j) in pairwise(row))):
            count_safe += 1
            print(row)
            continue
        for ind in range(len(row)):
            i_row = row[0:ind] + row[ind+1:]
            if all(abs(i - j) <= 3 for (i, j) in pairwise(i_row)) and (
                    all((i - j) > 0 for (i, j) in pairwise(i_row)) or all((i - j) < 0 for (i, j) in pairwise(i_row))):
                count_safe += 1
                print(i_row)
                break

    result_part2 = count_safe

    extra_out = {'Number of integer rows in input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
