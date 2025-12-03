from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=1, year=2025).data

    index = 50
    N = 100

    count_0_stop = 0
    count_0_all = 0
    for row in data:
        sign = 1 if row.startswith('R') else -1
        val = int(row[1:])

        # New value before getting remainder
        new = (index + sign * val)
        if new >= 100:
            count_0_all += new // 100
        if new < 0:  # If below 0: take abs but take into account you might have started at 0.
            count_0_all += abs(new) // 100 + (1 if index != 0 else 0)
        if new == 0:
            count_0_all += 1

        # Actual new index is same as new but then including getting the remainder
        index = (index + sign * val) % N
        if index == 0:
            count_0_stop += 1

    result_part1 = count_0_stop
    result_part2 = count_0_all

    extra_out = {'Number of rows in input': len(data)}

    return result_part1, result_part2, extra_out

if __name__ == "__main__":
    run_day(run_all, [1])
