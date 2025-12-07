from collections import defaultdict
from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=7, year=2025).data

    # Approach: keep track of splitters that are hit, and count the number of routes they can be hit, by going up
    # from it and checking if sideways there are hit splitters, until you reach a splitter directly up or end of grid.
    count = defaultdict(int)
    for i, row in enumerate(data):
        for j, el in enumerate(row):
            if el != '^':
                continue
            rw = i-1
            while rw >= 0:
                if rw + (j-1)*1j in count or rw + (j+1)*1j in count:
                    left = count[rw + j*1j - 1j] if rw + j*1j - 1j in count else 0  # Avoid creating entries
                    right = count[rw + j*1j + 1j] if rw + j*1j + 1j in count else 0  # Avoid creating entries
                    count[i+j*1j] += left + right
                elif data[rw][j] == 'S':
                    count[i+j*1j] += 1
                    break
                elif data[rw][j] == '^':
                    break
                rw -= 1

    # Repeat for final row to count how many routes there are to come to each location in final row
    final_count = 0
    for j, el in enumerate(data[-1]):
        rw = len(data) - 1
        while rw >= 0:
            if rw + j * 1j - 1j in count or rw + j * 1j + 1j in count:
                left = count[rw + j * 1j - 1j] if rw + j * 1j - 1j in count else 0
                right = count[rw + j * 1j + 1j] if rw + j * 1j + 1j in count else 0
                final_count += left + right
            elif data[rw][j] == 'S':
                final_count += 1
                break
            elif data[rw][j] == '^':
                break
            rw -= 1

    result_part1 = len(count.keys())  # Take set to deduplicate double-counting
    result_part2 = final_count

    extra_out = {'Size of grid': (len(data), len(data[0])),
                 'Number of splitters': sum(el=='^' for row in data for el in row)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
