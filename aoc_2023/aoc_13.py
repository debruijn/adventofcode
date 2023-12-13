from itertools import product
from typing import Union
from util.util import ProcessInput, run_day

debug = False


def do_check(data, n_row, skip=0):
    # Ugly 5-indent function to check whether a reflection line exists across rows. If so, return index of line.
    check = False
    for i in [i_ for i_ in range(1, n_row) if i_ != skip]:
        check_this = True
        if i < n_row - i:
            for j in range(1, i + 1):
                if data[i - j] != data[i + j - 1]:
                    check_this = False
                    break
        else:
            for j in range(n_row - i):
                if data[i - j - 1] != data[i + j]:
                    check_this = False
                    break
        if check_this:
            check = i
            break
    return check


def vert_to_hor(pattern, n_row, n_col):
    return [[pattern[i][j] for i in range(n_row)] for j in range(n_col)]


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=13, year=2023).as_list_of_strings_per_block().data

    total_sum_1 = 0
    total_sum_2 = 0
    for pattern in data:
        n_row = len(pattern)
        n_col = len(pattern[0])

        # Part 1: unadjusted; first check horizontal, then flip and check vertical
        hor_check = do_check(pattern, n_row)
        if not hor_check:
            pattern_flip = vert_to_hor(pattern, n_row, n_col)
            vert_check = do_check(pattern_flip, n_col)
        else:
            vert_check = 0
        total_sum_1 += 100 * hor_check + vert_check

        # Part 2: try each element to adjust; then do same approach as above but skip solution from above
        for i,j in product(range(n_row), range(n_col)):
            pattern_this = pattern.copy()
            if pattern_this[i][j] == '#':
                pattern_this[i] = pattern_this[i][:j] + '.' + pattern_this[i][j+1:]
            else:
                pattern_this[i] = pattern_this[i][:j] + '#' + pattern_this[i][j+1:]

            hor_check_2 = do_check(pattern_this, n_row, skip=hor_check)
            if not hor_check_2:
                pattern_flip = vert_to_hor(pattern_this, n_row, n_col)
                vert_check_2 = do_check(pattern_flip, n_col, skip=vert_check)
            else:
                vert_check_2 = 0
            pattern_check = 100 * hor_check_2 + vert_check_2

            if pattern_check:
                total_sum_2 += pattern_check
                break

    result_part1 = total_sum_1
    result_part2 = total_sum_2

    extra_out = {'Number of patterns in input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
