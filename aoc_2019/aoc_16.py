from typing import Union
from util.util import ProcessInput, run_day
from math import ceil

debug = False


def decode_signal(data):
    remaining_sum = sum(data)
    new = []
    for i in range(len(data)):
        new.append(abs(remaining_sum) % 10)
        remaining_sum -= data[i]
    return new


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=16, year=2019).data[0]

    R = 100
    curr = [int(x) for x in data]
    base_pattern = (0, 1, 0, -1)
    N = len(data)
    patterns = [(sum([[x]*i for x in base_pattern], [])*ceil((N+1)/len(base_pattern)))[1:N+1] for i in range(1, N+1)]

    for r in range(R):
        curr = [abs(sum([patterns[i][j] * curr[j] for j in range(N)])) % 10 for i in range(N)]

    result_part1 = int("".join(str(x) for x in curr[:8]))

    # Don't do it properly. For 2nd half of digits, new digits are sum of digits after it. Doesn't work for examples.
    data = [int(x) for x in data]
    loc = int("".join(map(str, data[:7])))
    if N * 10000/2 < loc <= N * 10000:
        data_postloc = (data * 10000)[loc:]
        for i in range(R):
            data_postloc = decode_signal(data_postloc)

        result_part2 = int("".join(str(x) for x in data_postloc[:8]))
    else:
        result_part2 = "N/A"

    extra_out = {'Number of elements in input': len(data)}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3])
