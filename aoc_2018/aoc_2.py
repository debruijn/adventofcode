from collections import Counter
from itertools import combinations
from typing import Union
from util.util import ProcessInput, run_day


def run_all(example_run: Union[int, bool]):

    data = ProcessInput(example_run=example_run, day=2, year=2018).data

    # Part 1
    counts = [0, 0]
    for id in data:
        counts = [counts[0] + any([x == 2 for x in Counter(id).values()]),
                  counts[1] + any([x == 3 for x in Counter(id).values()])]
    result_part1 = counts[0] * counts[1]

    # Part 2
    result_part2 = "TODO"
    len_ids = len(data[0])
    for id1, id2 in combinations(data, 2):
        if sum([id1[i] == id2[i] for i in range(len_ids)]) == len_ids - 1:
            result_part2 = "".join([id1[i] for i in range(len_ids) if id1[i] == id2[i]])
            break

    extra_out = {'Number of ids in input': len(data),
                 'Length of ids': len_ids}

    return result_part1, result_part2, extra_out


if __name__ == "__main__":
    run_day(run_all, [1])
