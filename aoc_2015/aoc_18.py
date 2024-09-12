from typing import Union
from util.util import ProcessInput, run_day


def run_light_grid(data, N, lights_fixed=False):

    L = len(data)  # dimension of grid

    # Convert to 1/0 incl padding to ease calculation
    states = [[0] + [1 if el == '#' else 0 for el in row] + [0] for row in data]
    states = [[0] * (L + 2)] + states + [[0] * (L + 2)]
    if lights_fixed:
        states[1][1], states[1][L], states[L][1], states[L][L] = 1, 1, 1, 1

    def check_loc(i, j):
        # Utility function to get the counts for a location (i,j) and return whether it will be a 1 or 0 after this iter
        count = sum(sum(row[j-1:j+2]) for row in states[i-1:i+2]) - states[i][j]
        if states[i][j] == 1:
            return 1 if count in (2, 3) else 0
        return 1 if count == 3 else 0

    for n in range(N):
        # Reassign the lights, again using the padding to make calculations easier.
        states = [[0] + [1 if check_loc(i, j) else 0 for j in range(1, L + 1)] + [0] for i in range(1, L + 1)]
        states = [[0] * (L + 2)] + states + [[0] * (L + 2)]
        if lights_fixed:
            states[1][1], states[1][L], states[L][1], states[L][L] = 1, 1, 1, 1

    return sum(sum(row) for row in states)


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=18, year=2015).data
    N = 4 if example_run else 100

    result_part1 = run_light_grid(data, N, lights_fixed=False)
    result_part2 = run_light_grid(data, N, lights_fixed=True)

    extra_out = {'Dimension of grid': (len(data), len(data[0]))}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
