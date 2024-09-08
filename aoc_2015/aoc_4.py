import hashlib
from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=4, year=2015).data[0].encode()
    index = 0
    found_five = False
    while True:
        this_hash = hashlib.md5((data + str(index).encode())).hexdigest()
        if this_hash.startswith('0' * 5):
            if not found_five:
                found_five = index
            if this_hash.startswith('0' * 6):
                break
        index +=1

    result_part1 = found_five
    result_part2 = index

    extra_out = {'Input to mining procedure': data}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [])  # No examples this time, to save run time since hashing is slow
