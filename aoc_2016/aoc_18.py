from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):
    # I have first tried implementing a history since I expected the same row to feature multiple times. Then we can
    # stop early, and calculate the remainder from the repeating loop.
    # - This happened for the 1st example, and in that case the code did what it should do
    # - But for the actual data, there was no recurring loop (for my input), so it was just doing the full 400000 loops
    #   but also keeping a history - removing that part resulted in a small performance boost.
    data = ProcessInput(example_run=example_run, day=18, year=2016).data
    row_len = len(data[0])

    count_safe = sum(x=='.' for x in data[0])
    count_safe_part1 = 'N/A'
    curr_row = "." + data[0] + "."  # Make algorithm easier by always adding safe spots at both ends

    R = 10 if example_run else 400000

    def is_trap(above):
        return True if above in ['^^.', '.^^', '^..', '..^'] else False

    for r in range(1, R):  # r == 0 is the input
        new_row_inner = ['^' if is_trap(curr_row[i-1:i+2]) else '.' for i in range(1, row_len + 1)]
        this_count = sum(x=='.' for x in new_row_inner)
        count_safe += this_count
        curr_row = '.' + "".join(new_row_inner) + '.'  # Again, add safe spots at both ends
        if r == 39:
            count_safe_part1 = count_safe

    result_part1 = count_safe_part1
    result_part2 = count_safe

    extra_out = {'Length of a row': row_len}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2])
