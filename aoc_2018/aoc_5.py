from itertools import pairwise
from typing import Union
from util.util import ProcessInput, run_day


def run_polymerization(polymer):
    stop = False
    curr_len = len(polymer)
    while not stop:
        for pair in pairwise(polymer):
            if ord(pair[0]) - ord(pair[1]) in [32, -32]:
                polymer = polymer.replace(pair[0]+pair[1], "")
        if len(polymer) == curr_len:
            stop = True
        curr_len = len(polymer)
    return curr_len


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=5, year=2018).data

    result_part1 = run_polymerization(data[0])

    best_len = result_part1
    for iter_types in range(26):  # Loop over all letters
        iter_remove = [chr(ord('A') + iter_types), chr(ord('a') + iter_types)]
        iter_polymer = data[0].replace(iter_remove[0], "").replace(iter_remove[1], "")
        iter_len = run_polymerization(iter_polymer)
        best_len = iter_len if iter_len < best_len else best_len

    result_part2 = best_len

    extra_out = {'Number of chars in input': len(data[0])}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1, 2, 3, 4, 5])
