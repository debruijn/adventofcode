from itertools import product
from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=25, year=2024).as_list_of_strings_per_block().data

    # Process input into column counts and assign to key or lock
    keys, locks = [], []
    for schematic in data:
        is_lock = (schematic[0] == '#' * len(schematic[0]))
        count = [0]*len(schematic[0])
        for row in schematic:
            for col, el in enumerate(row):
                if el == '#':
                    count[col] += 1
        locks.append(count) if is_lock else keys.append(count)

    # For all combinations of key and lock, find whether they have an overlap or not
    count_no_overlap = 0
    height = len(data[0])
    for key, lock in product(keys, locks):
        if all([key[i] + lock[i] <= height for i in range(len(key))]):
            count_no_overlap += 1

    result_part1 = count_no_overlap
    result_part2 = "Merry Christmas"

    extra_out = {'Number of keys in input': len(keys),
                 'Number of locks in input': len(locks),
                 'Length of keys and locks': len(data[0][0]),
                 'Height of keys and locks': height}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
