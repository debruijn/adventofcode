from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=17, year=2017).as_int().data[0]

    # Part 1: naive implementation in which we actually keep track of the full buffer, not knowing what is to come...
    N = 2017
    i = 0
    buffer = [0]
    for n in range(N):
        i = (i + data) % len(buffer)
        buffer = buffer[:i+1] + [n+1] + buffer[i+1:]
        i += 1
    result_part1 = buffer[buffer.index(2017)+1]

    # Part 2: only keep track of the number after 0. The number 0 is always at the start, so that is at location 1.
    N = 50000000
    i = 0
    len_buffer = 1
    last_at_1 = 0
    count_num_after_1 = 0
    for n in range(N):
        i = (i + data) % len_buffer
        if i == 0:
            last_at_1 = n + 1
            count_num_after_1 += 1
        i += 1
        len_buffer += 1

    result_part2 = last_at_1

    extra_out = {'Shift forward in each step of the algorithm': data,
                 'Number of times there is a new number after 0': count_num_after_1}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
