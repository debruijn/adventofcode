from typing import Union
from util.util import ProcessInput, run_day, batched


def get_checksum(state, req_length):
    curr_state = state
    while len(curr_state) < req_length:
        curr_state += '0' + "".join('1' if x == '0' else '0' for x in reversed(curr_state))

    checksum = curr_state[:req_length]
    while len(checksum) % 2 == 0:
        checksum = ['1' if x==y else '0' for x, y in batched(checksum, 2)]

    return "".join(checksum)


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=16, year=2016).data
    req_length = 272 if not example_run else 20 if example_run == 2 else 12

    result_part1 = get_checksum(data[0], req_length)
    result_part2 = "N/A" if example_run else get_checksum(data[0], 35651584)

    extra_out = {'Input string': data[0]}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2])
