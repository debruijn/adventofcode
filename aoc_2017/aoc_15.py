from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=15, year=2017).as_list_of_ints().data

    # Part 1: directly doing what is asked: updating each val each time and passing it to the check
    curr_val = data[0][0], data[1][0]
    mult = (16807, 48271)
    divisor = 2147483647

    N = 40000000
    n_match = 0
    for _ in range(N):
        curr_val = (curr_val[0] * mult[0]) % divisor, (curr_val[1] * mult[1]) % divisor
        if curr_val[0] % 65536 == curr_val[1] % 65536:  # Equivalent for checking equality of last 16 binary digits
            n_match += 1
    result_part1 = n_match

    # Part 2: keeping track of both generators whether they are ready to compare their next value
    curr_val = [data[0][0], data[1][0]]
    ready_to_compare = [False, False]

    N = 0
    n_match = 0
    while N < 5000000:
        if not ready_to_compare[0]:
            curr_val[0] = (curr_val[0] * mult[0]) % divisor
            if curr_val[0] % 4 == 0:
                ready_to_compare[0] = True
        if not ready_to_compare[1]:
            curr_val[1] = (curr_val[1] * mult[1]) % divisor
            if curr_val[1] % 8 == 0:
                ready_to_compare[1] = True
        if all(ready_to_compare):
            ready_to_compare = [False, False]
            N += 1
            if curr_val[0] % 65536 == curr_val[1] % 65536:
                n_match += 1

    result_part2 = n_match

    extra_out = {'Starting values': f"{data[0][0]}, {data[1][0]}"}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
